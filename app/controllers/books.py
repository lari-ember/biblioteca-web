from flask import request, redirect, flash, url_for, render_template, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from app import app, Book, db, UserBooks
from app.models.forms import BookForm
from app.models.code_book import generate_book_code


def create_book(user, form):
    """
    Cria e retorna um objeto Book baseado no formulário.
    """
    code = generate_book_code(form.genre.data, form.author.data, form.title.data)
    if not code:
        return None, "Genre not found. Please add a new genre."

    book = Book(
        isbn='1234',
        cover_url='4321',
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
