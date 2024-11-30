from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from app import User, app, lm, db
from app.models.forms import LoginForm, RegistrationForm


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Verificar se o nome de usuário já existe
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html', form=form)

        # Criar um novo usuário se o nome de usuário não existir
        user = User(
            username=form.username.data,
            password=form.password.data,
            name=form.name.data
        )

        # Hash da senha
        user.set_password(form.password.data)

        # Adicionar o usuário ao banco de dados
        db.session.add(user)
        db.session.commit()

        # Fazer login automático após o registro
        login_user(user)

        # Mensagem de sucesso e redirecionamento
        flash('Registration successful. You are now logged in.', 'success')
        return redirect(url_for('index'))

    # Renderizar o formulário de registro
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/logout')
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