from flask import Flask, current_app, render_template, request, redirect, flash, session, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from datetime import date
from app import app, User, db, lm, Book
from app.models.forms import LoginForm, RegistrationForm, BookForm
from app.models.code_book import generate_book_code
from flask_login import login_user, logout_user



@lm.user_loader
def load_user(user_id):
    # Implement the code to load the user from the database based on the user ID
    # Return the user object if found, or None if not found
    return User.query.get(int(user_id))


@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')


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
    # Clear the user's session
    logout_user()
    # Flash a message to notify the user
    flash('You have been logged out.', 'info')

    # Redirect the user to the desired page (e.g., home page)
    return redirect(url_for('index'))


@app.route('/insert_test_data')
def insert_test_data():
    # Create a User object with the desired test data
    user = User(username='test', password='password', name='Test Name')

    # Set the user's password (it will be automatically hashed)
    user.set_password('password')

    # Add the user to the database
    db.session.add(user)
    db.session.commit()

    return 'Test data inserted successfully!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # Create a new user object with form data
        print(f'{form.username.data}, {form.name.data} e {form.password.data}')
        user = User(
            username=form.username.data,
            password=form.password.data,
            name=form.name.data
        )

        # Set the user's password (it will be automatically hashed)
        user.set_password(form.password.data)

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        # Log in the newly registered user
        login_user(user)

        # Flash a success message and redirect to the home page
        flash('Registration successful. You are now logged in.', 'success')
        return redirect(url_for('index'))

    # Render the registration form
    return render_template('register.html', form=form)


from flask_login import current_user

def get_logged_in_user():
    if current_user.is_authenticated:
        return current_user
    else:
        # If the user is not logged in, you can return None or take any other action depending on your requirement.
        return None

@app.route('/register_new_book', methods=['GET', 'POST'])
def register_new_book():
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        user = get_logged_in_user()
        if user is None:
            flash('User is not authenticated', 'error')
            return redirect(url_for('login'))
        with current_app.app_context():
            code = generate_book_code(form.genre.data, form.author.data, form.title.data)
        if code is None:
            flash(f'Genre not found. Do you want to add a new genre?', 'warning')
            return redirect(url_for('index'))
        book = Book(
            user_id=user.id,
            code=code,
            author=form.author.data.lower(),
            title=form.title.data.lower(),
            publisher=form.publisher.data.lower(),
            year=form.year.data,
            pages=form.pages.data,
            read=form.read.data,
            genre=form.genre.data.lower(),
            status=form.status.data.lower(),
            format=form.format.data.lower()
            )
        db.session.add(book)
        db.session.commit()
        flash(f'New book registered successfully: title - {book.title} author - {book.author} code - {book.code} genre - {book.genre}', 'success')
        return redirect(url_for('your_collection'))
    else:
        print(request.method)
        print(form.validate())
        print(form.errors)
        print('not ok')
    return render_template('register_new_book.html', form=form)


@app.route('/your_collection')
def your_collection():
    # Verifique se o usuário está logado
    user = get_logged_in_user()
    if not user:
        # Redirecione para a página de login ou tome qualquer outra ação que você desejar para lidar com usuários não logados
        return redirect('/login')

    # Recupere os livros da tabela 'Book' para o usuário logado
    books = Book.query.filter_by(user_id=user.id).all()

    # Renderize o template 'your_collection.html' e passe os livros como 
    print(books)
    return render_template('your_collection.html', books=books)


@app.route('/delete_book/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
    else:
        flash('Book not found.', 'error')
    return redirect(url_for('your_collection'))
