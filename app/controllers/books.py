# books.py - Minimal working version
"""
Books controller - temporarily using old implementation while migration is prepared.
This ensures the app can start without errors.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db, cache
from app.models.modelsdb import Book, UserBooks
from app.models.forms import BookForm
from datetime import datetime

# Blueprint creation
books_bp = Blueprint('books', __name__, url_prefix='')


@books_bp.route('/register_new_book', methods=['GET', 'POST'])
@login_required
def register_new_book():
    """Temporary implementation - to be replaced with full CRUD version."""
    form = BookForm()

    if form.validate_on_submit():
        try:
            # Simple book creation without duplicate detection (temporary)
            # TODO: Replace with create_or_get_book() after migration
            flash('Book registration temporarily disabled during migration. Please try again later.', 'warning')
            return redirect(url_for('books.your_collection'))
        except Exception as e:
            current_app.logger.error(f"Error: {str(e)}")
            flash('An error occurred. Please try again.', 'danger')
            db.session.rollback()

    return render_template('books/register_new_book.html', form=form)


@books_bp.route('/your_collection', methods=['GET'])
@login_required
@cache.cached(timeout=300, query_string=True)
def your_collection():
    """Display user's book collection."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 20

        # Query user's books
        books_query = Book.query.join(UserBooks).filter(
            UserBooks.user_id == current_user.id
        ).order_by(Book.title.asc())

        paginated_books = books_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return render_template(
            'your_collection.html',
            books=paginated_books.items,
            pagination=paginated_books
        )

    except Exception as e:
        current_app.logger.error(f"Collection error: {str(e)}")
        flash('Error loading collection', 'danger')
        return redirect(url_for('core.index'))


# Placeholder routes to prevent import errors
# These will be replaced after migration

@books_bp.route('/autocomplete', methods=['GET'])
@login_required
def autocomplete():
    """Placeholder - to be implemented after migration."""
    from flask import jsonify
    return jsonify({'user_collection': [], 'shared_catalog': [], 'external_apis': []})


@books_bp.route('/add_to_collection/<int:book_id>', methods=['POST'])
@login_required
def add_to_collection(book_id):
    """Placeholder - to be implemented after migration."""
    flash('This feature will be available after migration', 'info')
    return redirect(url_for('books.your_collection'))


@books_bp.route('/view_book/<int:book_id>', methods=['GET'])
def view_book(book_id):
    """Placeholder - to be implemented after migration."""
    try:
        book = Book.query.get_or_404(book_id)
        return render_template('view_book.html', book=book)
    except Exception as e:
        flash('Book not found', 'error')
        return redirect(url_for('books.your_collection'))


@books_bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    """Placeholder - to be implemented after migration."""
    flash('Edit feature will be available after migration', 'info')
    return redirect(url_for('books.your_collection'))


@books_bp.route('/delete_book/<int:book_id>', methods=['POST', 'DELETE'])
@login_required
def delete_book(book_id):
    """Placeholder - to be implemented after migration."""
    flash('Delete feature will be available after migration', 'info')
    return redirect(url_for('books.your_collection'))


@books_bp.route('/search', methods=['GET'])
@login_required
def search():
    """Placeholder - to be implemented after migration."""
    return render_template('search.html', books=[], query='')

