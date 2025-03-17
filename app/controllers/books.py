# books.py
import traceback
from datetime import datetime

import requests
from flask import Blueprint
from flask import request, redirect, flash, url_for, render_template, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError

from app import db, cache
from app.models.book_search import get_book_cover_url, search_book_by_title
from app.models.code_book import generate_book_code
from app.models.forms import BookForm
from app.models.modelsdb import Book, UserBooks
from app.utils.helpers import flash_custom_errors
from app.utils.notifications import format_success_message

# Criação do Blueprint
books_bp = Blueprint('books', __name__, url_prefix='/books')

def create_book(user, form):
    """
        Cria um objeto Book validando dados, prevenindo duplicatas e garantindo consistência.

    Args:
        user (User): Objeto do usuário autenticado.
        form (BookForm): Formulário validado com dados do livro.

    Returns:
        tuple: (Book, None) em caso de sucesso | (None, str) com mensagem de erro.

    Raises:
        ValueError: Para dados inválidos ou regras de negócio violadas.
    """
    # Validação de campos obrigatórios
    required_fields = ['title', 'author', 'genre']
    for field in required_fields:
        if not getattr(form, field).data:
            return None, f"Field '{field}' is required."

    # Validação de dados numéricos
    try:
        if form.year.data < -5000 or form.year.data > datetime.now().year:
            raise ValueError("Invalid publication year")
        if form.pages.data < 1:
            raise ValueError("Page count must be at least 1")
    except TypeError:
        return None, "Invalid numeric format"

    # Geração de código com tratamento de erro
    try:
        code = generate_book_code(
            form.genre.data.strip().title(),
            form.author.data.strip(),
            form.title.data.strip()
        )
        if not code:
            return None, "Invalid genre. Use the predefined categories."
    except Exception as e:
        current_app.logger.error(f"Code generation error: {str(e)}")
        return None, "Error generating book code"

    # Busca de metadados com fallback
    try:
        isbn = search_book_by_title(form.title.data) or "ISBN-NOT-FOUND"
        cover_url = get_book_cover_url(isbn) or url_for('static', filename='images/default_cover.jpg')
    except Exception as e:
        current_app.logger.error(f"Metadata fetch error: {str(e)}")
        isbn = "ISBN-ERROR"
        cover_url = url_for('static', filename='images/default_cover.jpg')

    #code = generate_book_code(form.genre.data, form.author.data, form.title.data)

    #if not code:
    #    return None, "Genre not found. Please add a new genre."
    #isbn = search_book_by_title(form.title.data)

    # Construção do objeto com sanitização
    try:
        return Book(
            isbn=isbn[:17],  # Garante compatibilidade com campo de 17 caracteres
            cover_url=cover_url,
            user_id=user.id,
            code=code,
            title=form.title.data.strip(),
            author=form.author.data.strip().title(),  # Capitalização apropriada
            publisher=form.publisher.data.strip(),
            year=form.year.data,
            pages=form.pages.data,
            genre=form.genre.data.strip().capitalize(),
            format=form.format.data.strip().lower()
        ), None
    except Exception as e:
        current_app.logger.error(f"Book creation error: {str(e)}")
        return None, "Error creating book record"


@books_bp.route('/register_new_book', methods=['GET', 'POST'])
@login_required
def register_new_book():
    """Handle new book registration with comprehensive validation and error handling."""
    form = BookForm()
    try:
        if form.validate_on_submit():
            # Criar livro com validação adicional
            book, error = create_book(current_user, form)
            if error:
                flash(error, 'warning')
                return render_template('books/register_new_book.html', form=form), 400
            # Transação atômica com tratamento de concorrência
            with db.session.begin_nested():
                db.session.add(book)

            db.session.commit()

            # Redirecionamento seguro com pattern POST-REDIRECT-GET
            flash(format_success_message(book), 'success')
            return redirect(url_for('books.your_collection'))

            # Métricas e monitoramento
            track_metric('books_registered', 1)
            current_app.logger.info(f"Book {book.id} registered by {current_user.id}")

        elif request.method == 'POST':
            # Log detalhado para erros de validação
            current_app.logger.warning(f"Form validation errors: {form.errors}")
            flash_custom_errors(form)

    except SQLAlchemyError as e:
        handle_database_error(e)
        return render_template('books/register_new_book.html', form=form), 503

    except IntegrityError as e:
        handle_integrity_error(e)
        return redirect(url_for('books.register_new_book'))

    except Exception as e:
        current_app.logger.critical(f"Unexpected error: {traceback.format_exc()}")
        flash('A system error occurred. Please try again later.', 'danger')
        return redirect(url_for('main.index'))

    # Mantém dados do formulário após recarregamento
    preserve_form_state(form)
    return render_template('books/register_new_book.html', form=form)


@books_bp.route('/your_collection', methods=['GET'])
@login_required
@cache.cached(timeout=300, query_string=True)
def your_collection():
    """
    Exibe a coleção de livros do usuário com paginação e filtragem eficiente.

    Returns:
        Template renderizado com os livros do usuário ou redirecionamento em caso de erro.
    """
    try:
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = 10

        # Query otimizada com JOIN e filtragem
        books_query = Book.query.join(UserBooks).filter(
            UserBooks.user_id == current_user.id,
            Book.deleted == False  # Filtro para soft delete
        ).order_by(Book.title.asc())

        # Paginação
        paginated_books = books_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        current_app.logger.info(f"User {current_user.id} accessed collection with {paginated_books.total} books")

        return render_template(
            'your_collection.html',
            books=paginated_books.items,
            pagination=paginated_books
        )

    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error in your_collection: {str(e)}")
        flash('Error loading your collection. Please try again.', 'danger')
        return redirect(url_for('main.index'))

    except Exception as e:
        current_app.logger.critical(f"Unexpected error in your_collection: {traceback.format_exc()}")
        flash('A system error occurred. Please contact support.', 'danger')
        return redirect(url_for('main.index'))


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