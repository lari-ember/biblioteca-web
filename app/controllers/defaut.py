from flask import Flask, render_template, request, redirect, flash, session, url_for
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
        print(2)
        user = get_logged_in_user()
        if user is None:
            print(3)
            flash('User is not authenticated', 'error')
            return redirect(url_for('login'))  # Redirecionar para a página de login ou para outro local apropriado

        code = generate_book_code(form.genre.data)
        if code is None:
            print(1)
            flash('Genre not found. Do you want to add a new genre?', 'warning')
            # Redirecionar para uma página onde o usuário possa adicionar um novo gênero
            return redirect(url_for('add_genre'))

        book = Book(
            user_id=user.id,
            code=code,
            title=form.title.data.title(),
            author=form.author.data.title(),
            publisher=form.publisher.data.title(),
            year=form.year.data,
            pages=form.pages.data,
            genre=form.genre.data.title(),
            status=form.status.data.title(),
            format=form.format.data.title()
        )
        db.session.add(book)
        db.session.commit()
        print('ok')
        flash(f'New book registered successfully: Title - {book.title}, Author - {book.author}', 'success')
        return redirect(url_for('index'))
    else:
        print(request.method)
        print(form.validate())
        print('not ok')

    return render_template('register_new_book.html', form=form)



'''
    # Extract book information from the request form
    code = request.form['code']
    title = request.form['title']
    author = request.form['author']
    publisher = request.form['publisher']
    year = request.form['year']
    pages = request.form['pages']
    genre = request.form['genre']

    # Create a new Book object
    book = Book(user_id=user.id, code=code, title=title, author=author, publisher=publisher, year=year, pages=pages, genre=genre)

    # Add the book to the database
    db.session.add(book)
    db.session.commit()

    # Redirect the user to a success page or any other desired page
    return redirect('/success')'''
