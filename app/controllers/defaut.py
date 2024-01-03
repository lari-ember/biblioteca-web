import csv
from datetime import date, datetime

from flask import (Flask, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from sqlalchemy import or_
from sqlalchemy.sql import func

from app import Book, User, UserRead, UserReadings, app, db, lm
from app.models.code_book import book_genres, generate_book_code
from app.models.forms import (BookForm, EditReadingForm, LoginForm,
                              LogReadingForm, RegistrationForm, SearchForm)


def add_books_from_csv(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            book = Book(
                user_id=1,
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
            code = generate_book_code(
                form.genre.data, form.author.data, form.title.data)
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
        flash(
            f'New book registered successfully: title - {book.title} author - {book.author} code - {book.code} genre - {book.genre}', 'success')
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
                books = Book.query.filter(
                    field.ilike(f'%{search_term}%')).all()
        else:
            books = []

        return render_template('search.html', form=form, books=books)

    return render_template('search.html', form=form, books=[])


@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    # Verifique se o usuário está logado
    user = get_logged_in_user()
    if not user:
        # Redirecione para a página de login ou tome qualquer outra ação que você desejar para lidar com usuários não logados
        return redirect('/login')
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
                code = generate_book_code(
                    form.genre.data, form.author.data, form.title.data)
            if code != book.code:
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


@app.route('/about_your_library')
def about_your_library():
    user_readings = current_user.user_readings
    user = get_logged_in_user()
    if not user:
        # Redirecione para a página de login ou tome qualquer outra ação que você desejar para lidar com usuários não logados
        return redirect('/login')
        # Calcula a soma das páginas lidas nos livros já concluídos (UserRead)
    if db.session.query(func.sum(Book.pages)).filter(Book.read == 'read').scalar() != None:
        total_pages_completed = db.session.query(func.sum(Book.pages)).filter(Book.read == 'read').scalar()
    else:
        total_pages_completed = 0
    # Calcula a soma das páginas lidas nos livros em andamento (UserReadings)
    if db.session.query(func.sum(UserReadings.current_page)).filter(UserReadings.user_id == current_user.id).scalar() != None:
        total_pages_in_progress = db.session.query(func.sum(UserReadings.current_page)).filter(UserReadings.user_id == current_user.id).scalar()
    else:
        total_pages_in_progress = 0
    print(total_pages_completed)
    print(total_pages_in_progress)
    sum_pages = total_pages_in_progress + total_pages_completed
    genre_counts = db.session.query(Book.genre, func.count(Book.id)).group_by(Book.genre).all()
    return render_template('about_your_library.html', book_genres=book_genres, user_readings=user_readings, sum_pages=sum_pages, genre_counts=genre_counts)


@app.route('/add_to_current_readings/<int:book_id>', methods=['GET', 'POST'])
def add_to_current_readings(book_id):
    # Verifique se o livro existe na coleção do usuário
    book = Book.query.get(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('search'))

    # Verifique se o livro já está na tabela de leituras em andamento do usuário
    user_reading = UserReadings.query.filter_by(user_id=current_user.id, book_id=book.id).first()
    if user_reading:
        flash('Book already in current readings', 'error')
        return redirect(url_for('search'))

    # Adicione o livro à tabela de leituras em andamento
    user_reading = UserReadings(current_user.id, book.id, current_page=0, reading_percentage=0.0, time_spent=0, estimated_time=0)
    db.session.add(user_reading)
    db.session.commit()

    flash('Book added to current readings', 'success')
    return redirect(url_for('about_your_library'))

@app.route('/edit_reading/<int:reading_id>', methods=['GET', 'POST'])
@login_required  # Certifique-se de que o usuário esteja logado para acessar esta rota
def edit_reading(reading_id):
    user_reading = UserReadings.query.get(reading_id)
    if user_reading.user_id != current_user.id:
        # Certifique-se de que o usuário só pode editar suas próprias leituras
        flash('You do not have permission to edit this reading.', 'error')
        return redirect(url_for('about_your_library'))

    form = EditReadingForm(request.form)

    if request.method == 'POST' and form.validate():
        user_reading.current_page = form.current_page.data

# Verifique se o livro tem um número total de páginas válido (maior que zero)
        if user_reading.book.pages > 0:
            user_reading.reading_percentage = round((user_reading.current_page / user_reading.book.pages) * 100, 2)
            if user_reading.reading_percentage == 100:
                # Atualize o campo "read" na tabela de livros
                user_reading.book.read = 'read'
                user_reading.book.completion_date = datetime.now().strftime('%m-%d-%y')
                print(user_reading.book.completion_date)
                # Exclua o livro da tabela de leituras em andamento
                db.session.delete(user_reading)
        else:
            user_reading.reading_percentage = 0

        db.session.commit()
        flash('Reading information updated successfully!', 'success')
        return redirect(url_for('about_your_library'))

    # Passe o formulário e a leitura do usuário para o template de edição
    return render_template('edit_reading.html', form=form, user_reading=user_reading)


from flask import request


@app.route('/loan_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def loan_book(book_id):
    users = User.query.all()
    # Verifique se a solicitação é do tipo POST
    if request.method == 'POST':
    # Lógica para emprestar o livro
        book = Book.query.get(book_id)
        if book:
            if book.status == 'borrowed':
                flash('this book was borrowed.', 'warning')
            else:
                loan = Loan(
                    book_id=book.id,
                    borrower_id=current_user.id,
                    lender_id=current_user.id,  # Precisa ser atualizado com o ID do usuário atual
                    date_borrowed=date.today(),
                    due_date=date.today() + timedelta(days=15)  # Precisa ser calculada com base em um período definido
                            )
                db.session.add(loan)
                book.status = 'borrowed'  # Atualiza o status do livro para emprestado
                db.session.commit()
                flash('sucessfully borrowed book!', 'success')
        else:
            flash('book not found.', 'error')
            return redirect(url_for('your_collection', book_id=book_id))
        
    return render_template('loan_book.html', users=users, book_id=book_id)
