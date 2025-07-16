# books.py
import traceback
from datetime import datetime

import requests
from flask import Blueprint
from flask import request, redirect, flash, url_for, render_template, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app import db, cache
from app.models.book_search import get_book_cover_url, search_book_by_title
from app.models.code_book import generate_book_code
from app.models.forms import BookForm
from app.models.modelsdb import Book, UserBooks
from app.utils.helpers import flash_custom_errors
from app.utils.notifications import format_success_message
from app.utils.sanitize import sanitize_string

# Criação do Blueprint
books_bp = Blueprint('books', __name__, url_prefix='')

def create_book(form):
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
        return None, "Invalid numeric format."

    # Geração de código com tratamento de erro
    try:
        code = generate_book_code(
            sanitize_string(form.genre.data, 'title'),
            sanitize_string(form.author.data),
            sanitize_string(form.title.data)
        )
        if not code:
            return None, "Invalid genre. Use the predefined categories."
    except Exception as e:
        current_app.logger.error(f"Code generation error: {str(e)}")
        return None, "Error generating book code."

    # Busca de metadados com fallback
    raw_isbn = None
    try:
        raw_isbn = search_book_by_title(form.title.data)
        if raw_isbn == 'Na':
            raw_isbn = None
    except Exception as e:
        current_app.logger.error(f"Metadata fetch error: {e}")
    # Se o formulário tiver campo isbn, leia-o; senão, None
    user_isbn = getattr(form, 'isbn', None) and form.isbn.data.strip()

    # Define ISBN a usar
    isbn_candidate = raw_isbn
    isbn = None
    if isbn_candidate:
        clean = isbn_candidate.replace('-', '').strip()
        if len(clean) == 13 and clean.isdigit():
            isbn = clean
        else:
            return None, f"{raw_isbn} Invalid ISBN: must be exactly 13 numeric digits."
    try:
        cover_url = get_book_cover_url(isbn) or url_for('static', filename='images/default_cover.jpg')
    except Exception as e:
        cover_url = url_for('static', filename='images/default_cover.jpg')

    # Construção do objeto com sanitização
    try:
        return Book(
            isbn=isbn,
            cover_url=cover_url,
            code=code,
            title=sanitize_string(form.title.data),
            author=sanitize_string(form.author.data, 'title'),
            publisher=sanitize_string(form.publisher.data),
            publication_year=form.year.data,
            pages=form.pages.data,
            genre=sanitize_string(form.genre.data, 'capitalize'),
            format=sanitize_string(form.format.data, 'lower')
        ), None
    except Exception as e:
        current_app.logger.error(f"Book creation error: {str(e)}")
        return None, "Error creating book record."


@books_bp.route('/register_new_book', methods=['GET', 'POST'])
@login_required
def register_new_book():
    """Handle new book registration with comprehensive validation and error handling."""
    form = BookForm()
    try:
        if form.validate_on_submit():
            # Criar livro com validação adicional
            book, error = create_book(form)
            if error:
                flash(error, 'warning')
                return render_template('books/register_new_book.html', form=form), 400
            # Transação atômica com tratamento de concorrência
            with db.session.begin_nested():
                db.session.add(book)
                # faz flush para garantir que book.id seja gerado
                db.session.flush()


                # 2) cria o vínculo UserBooks
                user_book = UserBooks(
                    user_id=current_user.id,
                    book_id=book.id,
                    status='available',
                    acquisition_date=datetime.utcnow()
                )
                db.session.add(user_book)

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
        from app.utils.helpers import handle_database_error
        current_app.logger.error(f"Database error in register_new_book: {str(e)}")
        return render_template('books/register_new_book.html', form=form), 503

    except IntegrityError as e:
        # Tratamento específico para erros de integridade
        current_app.logger.error(f"Integrity error in register_new_book: {str(e)}")
        return redirect(url_for('books.register_new_book'))

    except Exception as e:
        current_app.logger.critical(f"Unexpected error: {traceback.format_exc()}")
        flash('A system error occurred. Please try again later.', 'danger')
        return redirect(url_for('main.index'))

    # Mantém dados do formulário após recarregamento
    return render_template('books/register_new_book.html', form=form)


@books_bp.route('/your_collection', methods=['GET'])
@login_required
@cache.cached(timeout=300, query_string=True)
def your_collection():
    """
    Exibe a coleção de livros do usuário com paginação e filtragem eficiente.

    Returns:
        Modelo renderizado com os livros do usuário ou redirecionamento em caso de erro.
    """
    try:
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = 10

        # Query otimizada com JOIN e filtragem
        books_query = Book.query.join(UserBooks).filter(
            UserBooks.user_id == current_user.id
            #Book.deleted == False  # Filtro para soft delete
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
        return redirect(url_for('core.index'))


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