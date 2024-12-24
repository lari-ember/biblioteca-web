import csv
from datetime import date, datetime, timedelta

import requests
from flask import (current_app, flash, redirect, render_template,
                   request, url_for)
from flask import jsonify
from flask_login import (current_user, login_required)
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.sql import func

from app import Book, User, UserReadings, Loan, app
from app import db
from app.controllers.auth import get_logged_in_user
from app.models.book_search import get_book_cover_url
from app.models.book_search import search_book_by_title
from app.models.code_book import book_genres, generate_book_code
from app.models.forms import (BookForm, EditReadingForm, SearchForm)


def add_books_from_csv(file_path):
    """
    Lê um arquivo CSV e adiciona livros ao banco de dados.
    Faz uso de `get_book_info` e `get_book_cover_url` para obter informações adicionais.
    """
    try:
        print('tentando')
        with open(file_path, 'r', encoding='UTF-8') as file:
            reader = csv.DictReader(file)
            books_to_add = []
            print('tentando')
            for row in reader:
                print('tentando')
                try:
                    # Obtém informações do livro pelo ISBN
                    isbn = row.get('titulo', '').strip()
                    book_info = search_book_by_title(isbn) if isbn else None

                    # Obtém a URL da capa do livro
                    cover_url = get_book_cover_url(book_info) if book_info else None

                    # Cria uma instância do livro
                    book = Book(
                        user_id=1,  # Ajuste se necessário
                        code=row.get('codigo', 'er000').strip(),
                        title=row.get('titulo', 'Desconhecido'),
                        author=row.get('autore', 'Desconhecido'),
                        publisher=row.get('editora', 'comunismo'),
                        year=int(row.get('ano', 2024)),
                        pages=row.get('paginas', 0),
                        genre=row.get('genero', 'General'),
                        format=row.get('formato', 'Desconhecido'),
                        cover_url=cover_url,
                        isbn=book_info
                    )
                    db.session.add(book)
                    db.session.commit()
                    print('esse foi')
                except Exception as e:
                    print(f"Erro ao processar o registro {row}: {e}")
    except Exception as e:
        print(f"Erro ao importar livros do CSV: {e}")
        db.session.rollback()


# Caminho para o arquivo CSV de exemplo
csv_file_path = 'acervo.csv'


@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
    #db.session.query(Book).delete()
    #db.session.commit()
    #add_books_from_csv(csv_file_path)
    return render_template('index.html')


def fetch_openlibrary_books(query, limit):
    """
    Busca livros na API da OpenLibrary.
    Limita os resultados para a quantidade especificada em `limit`.
    """
    url = f"https://openlibrary.org/search.json?q={query}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = []
        for doc in data.get('docs', []):
            results.append({
                'title': doc.get('title'),
                'author': ', '.join(doc.get('author_name', [])),
                'cover_url': f"https://covers.openlibrary.org/b/id/{doc.get('cover_i', '0')}-M.jpg" if doc.get('cover_i') else None,
                'genre': ', '.join(doc.get('subject', [])) if 'subject' in doc else 'General',
                'year': doc.get('first_publish_year', '2024'),
                'isbn': doc.get('isbn', [''])[0]
            })
        return results
    return []

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').strip()
    if query:
        # Busca livros no banco local
        local_books = Book.query.filter(Book.title.ilike(f'%{query}%')).limit(10).all()

        # Calcula a quantidade de resultados faltantes
        remaining = 10 - len(local_books)

        # Se faltar resultados, busca na OpenLibrary
        suggestions = []
        if remaining > 0:
            suggestions = fetch_openlibrary_books(query, remaining)

        # Retorna os resultados separados
        return jsonify({
            "local": [
                {
                    "title": book.title,
                    "author": book.author,
                    "cover_url": book.cover_url,
                    "genre": book.genre,
                    "year": book.year
                }
                for book in local_books
            ],
            "suggestions": suggestions
        })
    return jsonify({"local": [], "suggestions": []})  # Lista vazia caso não haja consulta


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
    #'read': Book.read,
    #'status': Book.status,
    'format': Book.format,
    'publisher': Book.publisher
}


@app.route('/search', methods=['GET', 'POST'])
def search():
        # Verifique se o usuário está logado
    user = get_logged_in_user()
    if not user:
        # Redirecione para a página de login ou tome qualquer outra ação que você desejar para lidar com usuários não logados
        return redirect('/login')
    form = SearchForm()

    if form.validate_on_submit():
        search_field = form.search_field.data
        search_term = form.search_term.data

        # Obtém o usuário logado
        user = get_logged_in_user()

        if user:
            # Realize a pesquisa com base nos dados fornecidos
            if search_field and search_field in field_mapping:
                field = field_mapping[search_field]
                if search_field == 'pages' or search_field == 'year':
                    # Realize a pesquisa com base em um valor numérico
                    try:
                        search_term = int(search_term)
                        books = Book.query.filter(
                            (field == search_term) &
                            (Book.user_id == user.id)
                        ).all()
                    except ValueError:
                        books = []
                else:
                    # Realize a pesquisa com base em uma string
                    books = Book.query.filter(
                        (field.ilike(f'%{search_term}%')) &
                        (Book.user_id == user.id)
                    ).all()
            else:
                books = []
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
            with current_app.app_context():
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
    user = get_logged_in_user()
    if not user:
        # Redirecione para a página de login ou tome qualquer outra ação que você desejar para lidar com usuários não logados
        return redirect('/login')
        # Calcula a soma das páginas lidas nos livros já concluídos (UserRead)
    user_readings = current_user.user_readings
    if db.session.query(func.sum(Book.pages)).filter(Book.read == 'read').scalar() != None:
        total_pages_completed = db.session.query(
            func.sum(Book.pages)).filter(Book.read == 'read').scalar()
    else:
        total_pages_completed = 0
    # Calcula a soma das páginas lidas nos livros em andamento (UserReadings)
    if db.session.query(func.sum(UserReadings.current_page)).filter(UserReadings.user_id == current_user.id).scalar() != None:
        total_pages_in_progress = db.session.query(func.sum(UserReadings.current_page)).filter(
            UserReadings.user_id == current_user.id).scalar()
    else:
        total_pages_in_progress = 0
    sum_pages = total_pages_in_progress + total_pages_completed
    current_user.update_sum_pages()
    genre_counts = db.session.query(
        Book.genre, func.count(Book.id)).group_by(Book.genre).all()
    borrowed_books = Book.query.filter(
    or_(Book.status == 'borrowed', Book.status == 'voluit'), Book.user_id == current_user.id).all()
    return render_template('about_your_library.html', book_genres=book_genres, user_readings=user_readings, sum_pages=sum_pages, genre_counts=genre_counts, borrowed_books=borrowed_books)


@app.route('/add_to_current_readings/<int:book_id>', methods=['GET', 'POST'])
def add_to_current_readings(book_id):
    # Verifique se o livro existe na coleção do usuário
    book = Book.query.get(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('search'))

    # Verifique se o livro já está na tabela de leituras em andamento do usuário
    user_reading = UserReadings.query.filter_by(
        user_id=current_user.id, book_id=book.id).first()
    if user_reading:
        flash('Book already in current readings', 'error')
        return redirect(url_for('search'))

    # Adicione o livro à tabela de leituras em andamento
    user_reading = UserReadings(current_user.id, book.id, current_page=0,
                                reading_percentage=0.0, time_spent=0, estimated_time=0)
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
            user_reading.reading_percentage = round(
                (user_reading.current_page / user_reading.book.pages) * 100, 2)
            if user_reading.reading_percentage == 100:
                # Atualize o campo "read" na tabela de livros
                user_reading.book.read = 'read'
                user_reading.book.completion_date = datetime.now().strftime('%m-%d-%y')
                # Exclua o livro da tabela de leituras em andamento
                db.session.delete(user_reading)
        else:
            user_reading.reading_percentage = 0

        db.session.commit()
        flash('Reading information updated successfully!', 'success')
        return redirect(url_for('about_your_library'))

    # Passe o formulário e a leitura do usuário para o template de edição
    return render_template('edit_reading.html', form=form, user_reading=user_reading)


@app.route('/loan_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def loan_book(book_id):
    users = User.query.all()
    if request.method == 'POST':
        book = Book.query.get(book_id)
        if book:
            if book.status == 'borrowed':
                flash('This book is already borrowed.', 'warning')
            else:
                # Get the lender ID from the selected user (borrower ID should already be current_user.id)
                # Assuming you have a form field to select a user
                selected_user_id = request.form.get('borrower')
                if not selected_user_id:
                    flash('Please select a user to borrow the book.', 'error')
                    return redirect(url_for('loan_book', book_id=book_id))
                else:
                    loan = Loan(
                        book_id=book.id,
                        borrower_id=current_user.id,
                        lender_id=selected_user_id,  # Update with the selected user's ID
                        date_borrowed=date.today(),
                        due_date=date.today() + timedelta(days=15)
                    )
                    book.loan_id = loan.id  # Atualiza o livro emprestado com o ID do empréstimo
                    db.session.add(loan)
                    book.status = 'borrowed'
                    book_borrowed = Book(
                        user_id=selected_user_id,
                        code=f'B-> {book.code}',
                        title=book.title,
                        author=book.author,
                        publisher=book.publisher,
                        year=book.year,
                        pages=book.pages,
                        genre=book.genre,
                        format=book.format,
                        read='unread',
                        status='voluit',
                    )
                db.session.add(book_borrowed)
                db.session.commit()
                flash('Successfully borrowed the book!', 'success')
        else:
            flash('Book not found.', 'error')
        return redirect(url_for('close_window'))

    return render_template('loan_book.html', users=users, book_id=book_id)


@app.route('/close_window/', methods=['GET', 'POST'])
@login_required
def close_window():
    return render_template('close_window.html')


@app.route('/change_status/<int:book_id>', methods=['POST'])
@login_required
def change_status(book_id):
    new_status = request.json.get('newStatus')

    book = Book.query.get(book_id)
    if book:
        book.status = new_status
        db.session.commit()
        # Filtrar os livros pelo ID do usuário e pelo status "voluit"
        loan = Loan.query.filter_by(book_id=book_id).first()
        if loan:
            old_owner_id = loan.lender_id
            old_owner = User.query.get(old_owner_id)
            book_with_status_voluit = Book.query.filter(and_(Book.user_id == old_owner.id, Book.status == 'voluit')).first()
            if book_with_status_voluit:
                db.session.delete(book_with_status_voluit)
                db.session.commit()
                db.session.delete(loan)  # Exclua o registro de empréstimo
                db.session.commit()
        return 'Status updated successfully', 200
    else:
        return 'Book not found', 404



@app.route('/profile/')
def profile():
    return render_template('profile.html')
