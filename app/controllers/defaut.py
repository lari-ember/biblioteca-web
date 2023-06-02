import csv
from flask import Flask, current_app, render_template, request, redirect, flash, session, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from datetime import date

from sqlalchemy import or_
from app import app, User, db, lm, Book
from app.models.forms import LoginForm, RegistrationForm, BookForm, SearchForm
from app.models.code_book import generate_book_code
from flask_login import login_user, logout_user


def add_books_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            book = Book(
                user_id= 1,
                code=row['codigo'],
                title=row['titulo'],
                author=row['autore'],
                publisher=row['editora'],
                year=row['ano'],
                pages=row['paginas'],
                read=row['lido'],
                genre=row['genero'],
                status=row['possui'],
                format=row['formato']
            )
            db.session.add(book)
            db.session.commit()

# Caminho para o arquivo CSV de exemplo
csv_file_path = 'C:/Users/bolsista.SFDA-DOACAO-BOL/Documents/GitHub/Biblioteca/acervo.csv'


@lm.user_loader
def load_user(user_id):
    #add_books_from_csv(csv_file_path)
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


def is_admin_user():
    # Implemente sua lógica aqui para determinar se o usuário é um administrador
    # Por exemplo, você pode verificar se o ID do usuário corresponde ao ID de um administrador na base de dados
    user_id = get_logged_in_user()
    admin_ids = [1, 2, 3]  # IDs dos usuários administradores

    if user_id in admin_ids:
        return True
    else:
        return False


# Mapeamento dos campos de pesquisa aos atributos do modelo Book
field_mapping = {
    'code': Book.code,
    'title': Book.title,
    'author': Book.author,
    'pages': Book.pages,
    'year': Book.year,
    'genre': Book.genre,
    'read': Book.read,
    'status': Book.status,
    'format': Book.format,
    'publisher': Book.publisher
}


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        search_field = form.search_field.data
        search_term = form.search_term.data

        # Realize a pesquisa com base nos dados fornecidos
        if search_field and search_field in field_mapping:
            field = field_mapping[search_field]
            if search_field == 'pages' or search_field == 'year':
                # Realize a pesquisa com base em um valor numérico
                try:
                    search_term = int(search_term)
                    books = Book.query.filter(field == search_term).all()
                except ValueError:
                    books = []
            else:
                # Realize a pesquisa com base em uma string
                books = Book.query.filter(field.ilike(f'%{search_term}%')).all()
        else:
            books = []

        return render_template('search.html', form=form, books=books)

    return render_template('search.html', form=form, books=[])


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm()

    if form.validate_on_submit():
        user = get_logged_in_user()
        if user is None:
            flash('User is not authenticated', 'error')
            return redirect(url_for('login'))
        if book.genre != form.genre.data:
            print(book.genre)
            print(form.genre.data)
            with current_app.app_context():
                print(form.author.data)
                code = generate_book_code(form.genre.data, form.author.data, form.title.data)
            if code != book.code:
                print('aaaaaaaaaaaaaaaaaaaa')
                print(book.code)
                print('bbbbbbbbbbbb')
                print(code)
                book.code = code
        if code is None:
            flash(f'Genre not found. Do you want to add a new genre?', 'warning')
            return redirect(url_for('index'))
        book.title = form.title.data
        book.author = form.author.data
        book.publisher = form.publisher.data
        book.year = form.year.data
        book.pages = form.pages.data
        book.read = form.read.data
        book.genre = form.genre.data
        book.status = form.status.data
        book.format = form.format.data

        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('your_collection'))

    return render_template('edit_book.html', form=form, book=book)

