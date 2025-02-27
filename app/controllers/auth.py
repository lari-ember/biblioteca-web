# controllers/auth.py
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash

from app import db, lm
from app.models.forms import RegistrationForm, LoginForm
from app.models.modelsdb import User
from app.utils.security import validate_password_complexity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


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
            return redirect(url_for('main.index'))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            # Logar o erro para monitoramento
            app.logger.error(f'Registration error: {str(e)}')

    elif request.method == 'POST':
        # Lidar com erros de validação do formulário
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'danger')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@lm.user_loader
def load_user(user_id):
    #add_books_from_csv(csv_file_path)
    # Implement the code to load the user from the database based on the user ID
    # Return the user object if found, or None if not found
    return User.query.get(int(user_id))


def get_logged_in_user():
    if current_user.is_authenticated:
        return current_user
    else:
        # If the user is not logged in, you can return None or take any other action depending on your requirement.
        return None