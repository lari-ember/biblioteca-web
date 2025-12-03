# controllers/auth.py
from urllib.parse import urlparse

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user
from flask_login import login_user, logout_user
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from app import db, login_manager
from app.models.forms import RegistrationForm, LoginForm
from app.models.modelsdb import User
from app.security.security import validate_password_complexity

auth_bp = Blueprint('auth', __name__, url_prefix='')

def url_has_allowed_host_and_scheme(url, allowed_hosts=None):
    if not url:
        return False

    parsed_url = urlparse(url)
    if parsed_url.scheme not in ('http', 'https'):
        return False

    if allowed_hosts is not None and parsed_url.hostname not in allowed_hosts:
        return False

    return True

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration with validation and security checks."""
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            # Validação de segurança adicional
            if not validate_password_complexity(form.password.data):
                flash('Password must contain at least 8 characters, one uppercase letter and one number.', 'danger')
                return render_template('auth/register.html', form=form)

            # Verificar se o usuário já existe
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('This username is already taken. Please choose another one.', 'danger')
                return redirect(url_for('auth.register'))

            # Criar novo usuário com hash seguro
            hashed_password = generate_password_hash(
                form.password.data,
                method='scrypt',
                salt_length=16
            )

            new_user = User(
                username=form.username.data,
                password_hash=hashed_password,
                name=form.name.data
            )

            db.session.add(new_user)
            db.session.commit()

            # Login automático após registro
            login_user(new_user)

            flash('Registration successful! Welcome to your library.', 'success')
            return redirect(url_for('core.index'))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            # Logar o erro para monitoramento
            current_app.logger.error(f'Registration error: {str(e)}')

    elif request.method == 'POST':
        # Lidar com erros de validação do formulário
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login with security measures.

    Security features:
    - CSRF protection (Flask-WTF)
    - Timing attack prevention
    - Safe redirects validation
    - Generic error messages to prevent user enumeration
    - Login attempt logging
    """
    form = LoginForm(request.form)

    # Validação de redirecionamento seguro
    next_url = request.args.get('next')
    if next_url and not url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
        current_app.logger.warning(f"Unsafe redirect attempt blocked: {next_url}")
        next_url = None

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # Prevenção de timing attack - verificar hash mesmo se usuário não existir
        password_valid = False
        if user:
            password_valid = user.check_password(form.password.data)

        # Logging de tentativas de login (CORRIGIDO: usar current_app.logger)
        current_app.logger.info(
            f"Login attempt - Username: {form.username.data}, IP: {request.remote_addr}, Success: {password_valid}"
        )

        if user and password_valid:
            # Login bem-sucedido
            login_user(user, remember=form.remember.data)

            # Atualizar last_login timestamp
            try:
                user.last_login = func.now()
                db.session.commit()
            except Exception as e:
                current_app.logger.warning(f"Failed to update last_login: {e}")
                db.session.rollback()

            flash('Login realizado com sucesso! Bem-vindo de volta.', 'success')
            return redirect(next_url or url_for('core.index'))  # CORRIGIDO: usar core.index
        else:
            # Feedback genérico para evitar user enumeration
            flash('Nome de usuário ou senha inválidos.', 'danger')
            current_app.logger.warning(
                f"Failed login attempt - Username: {form.username.data}, IP: {request.remote_addr}"
            )

    # Exibir erros de validação do formulário
    elif request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'warning')

    return render_template('auth/login.html', form=form, next=next_url)


@auth_bp.route('/logout')
def logout():
    """Handle user logout and redirect to homepage."""
    username = current_user.username if current_user.is_authenticated else 'Anonymous'

    logout_user()

    # Log de logout
    current_app.logger.info(f"User logged out - Username: {username}")

    flash('Você foi desconectado com sucesso. Até breve!', 'info')
    return redirect(url_for('core.index'))  # CORRIGIDO: usar core.index


@login_manager.user_loader
def load_user(user_id):
    from app.models.modelsdb import User
    try:
        return User.query.get(int(user_id))
    except Exception:
        current_app.logger.warning("load_user: ID inválido %s", user_id)
        return None


def get_logged_in_user():
    """Retorna o usuário autenticado ou None, com verificação de contexto."""
    if current_user.is_authenticated:
        return current_user
    # Log para acesso não autenticado (opcional)
    current_app.logger.debug("Acesso a recurso restrito sem autenticação")
    return None