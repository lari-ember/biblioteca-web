import requests
from flask import request, redirect, flash, url_for, render_template
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from app import app, Book, db, UserBooks
from app.models.book_search import get_book_cover_url, search_book_by_title
from app.models.code_book import generate_book_code
from app.models.forms import BookForm


def create_book(user, form):
    """
    Cria e retorna um objeto Book baseado no formulário.
    """
    code = generate_book_code(form.genre.data, form.author.data, form.title.data)
    if not code:
        return None, "Genre not found. Please add a new genre."
    isbn = search_book_by_title(form.title.data)

    book = Book(
        isbn=isbn,
        cover_url=get_book_cover_url(isbn),
        user_id=user.id,
        code=code,
        author=form.author.data.lower(),
        title=form.title.data.lower(),
        publisher=form.publisher.data.lower(),
        year=form.year.data,
        pages=form.pages.data,
        genre=form.genre.data.lower(),
        format=form.format.data.lower()
    )
    return book, None


@app.route('/register_new_book', methods=['GET', 'POST'])
@login_required
def register_new_book():
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():
        # Gera o livro a partir do formulário
        book, error_message = create_book(current_user, form)
        if error_message:
            flash(error_message, 'warning')
            return redirect(url_for('register_new_book'))

        try:
            # Adiciona o livro ao banco de dados
            db.session.add(book)
            db.session.commit()
            flash(f'New book registered successfully: {book.title} by {book.author}', 'success')
            return redirect(url_for('your_collection'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'An error occurred while registering the book: {str(e)}', 'error')
            return redirect(url_for('register_new_book'))

    return render_template('register_new_book.html', form=form)


@app.route('/your_collection')
@login_required
def your_collection():
    # Busca os livros associados ao usuário atual por meio da tabela intermediária UserBooks
    user_books = UserBooks.query.filter_by(user_id=current_user.id).all()
    books = [ub.book for ub in user_books]  # Obtém os objetos de livros associados
    return render_template('your_collection.html', books=books)


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