# books.py - Minimal working version
"""
Books controller - temporarily using old implementation while migration is prepared.
This ensures the app can start without errors.
"""
import time

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app import db, cache, limiter
from app.models.modelsdb import Book, UserBooks
from app.models.forms import BookForm
from app.services.openlibrary_service import get_openlibrary_service
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
@limiter.limit("100 per minute")
def autocomplete():
    """
    Autocomplete endpoint combining local DB search and OpenLibrary API.

    Returns results in two categories:
    - local: Books already in user's collection
    - suggestions: Books from OpenLibrary API

    Supports pagination via `offset` parameter (default 0).
    Returns `page_size` items per request (default 3), prioritizing local matches.
    Includes `has_more` flag and performance metrics in response.
    """
    start_time = time.time()
    query = request.args.get('query', '').strip()
    offset = request.args.get('offset', 0, type=int)
    page_size = request.args.get('page_size', 3, type=int)

    # Clamp page_size between 1 and 10
    page_size = max(1, min(page_size, 10))

    if not query or len(query) < 2:
        return jsonify({
            'local': [],
            'suggestions': [],
            'metadata': {
                'total': 0,
                'has_more': False,
                'offset': 0,
                'response_time_ms': 0
            }
        })

    try:
        # Step 1: Search user's local collection (always prioritized)
        search_filters = [
            Book.title.ilike(f'%{query}%'),
            Book.author.ilike(f'%{query}%'),
        ]
        # Add ISBN search if query looks like a number
        if query.replace('-', '').replace(' ', '').isdigit():
            search_filters.append(Book.isbn.ilike(f'%{query}%'))

        local_books = Book.query.join(UserBooks).filter(
            UserBooks.user_id == current_user.id,
            db.or_(*search_filters)
        ).limit(15).all()

        all_local = [
            {
                'title': book.title,
                'author': book.author,
                'cover_url': book.cover_url,
                'genre': book.genre,
                'year': book.publication_year,
                'publisher': book.publisher,
                'pages': book.pages,
                'isbn': book.isbn,
                'source': 'local'
            }
            for book in local_books
        ]

        # Step 2: Search OpenLibrary API for additional suggestions
        all_suggestions = []
        remaining_for_api = max(0, 15 - len(all_local))

        if remaining_for_api > 0:
            try:
                ol_service = get_openlibrary_service()
                api_results = ol_service.search_books(query, limit=remaining_for_api)

                all_suggestions = [
                    {
                        'title': item['title'],
                        'author': item['author'],
                        'cover_url': item['cover_url'],
                        'fallback_urls': item.get('fallback_urls', []),
                        'genre': item['genre'],
                        'year': item['year'],
                        'publisher': item['publisher'],
                        'pages': item.get('pages', 0),
                        'isbn': item.get('isbn'),
                        'openlibrary_key': item.get('openlibrary_key'),
                        'source': 'openlibrary'
                    }
                    for item in api_results
                ]
            except Exception as api_err:
                current_app.logger.warning(f"OpenLibrary fallback error: {api_err}")

        # Step 3: Merge all results (local first, then suggestions)
        all_results = all_local + all_suggestions
        total_available = len(all_results)

        # Step 4: Apply pagination window
        page_results = all_results[offset:offset + page_size]
        has_more = (offset + page_size) < total_available

        # Split paginated results back into local/suggestions for frontend
        local_page = [r for r in page_results if r.get('source') == 'local']
        suggestions_page = [r for r in page_results if r.get('source') == 'openlibrary']

        # Calculate response time
        response_time_ms = (time.time() - start_time) * 1000

        response = {
            'local': local_page,
            'suggestions': suggestions_page,
            'metadata': {
                'total': total_available,
                'local_count': len(all_local),
                'api_count': len(all_suggestions),
                'offset': offset,
                'page_size': page_size,
                'has_more': has_more,
                'response_time_ms': round(response_time_ms, 2),
                'query': query
            }
        }

        current_app.logger.info(
            f"Autocomplete: query='{query}' offset={offset} "
            f"local={len(local_page)}/{len(all_local)} "
            f"api={len(suggestions_page)}/{len(all_suggestions)} "
            f"has_more={has_more} time={response_time_ms:.2f}ms"
        )

        return jsonify(response)

    except Exception as e:
        current_app.logger.error(f"Autocomplete error: {str(e)}")
        return jsonify({
            'local': [],
            'suggestions': [],
            'metadata': {
                'total': 0,
                'has_more': False,
                'error': str(e),
                'response_time_ms': (time.time() - start_time) * 1000
            }
        }), 500


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

