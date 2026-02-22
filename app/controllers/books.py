# books.py - Minimal working version
"""
Books controller - temporarily using old implementation while migration is prepared.
This ensures the app can start without errors.
"""
import json
import os
import time

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from app import db, cache, limiter
from app.models.modelsdb import Book, UserBooks
from app.models.forms import BookForm
from app.services.openlibrary_service import get_openlibrary_service
from app.models.code_book import generate_book_code
from datetime import datetime

# Blueprint creation
books_bp = Blueprint('books', __name__, url_prefix='')


@books_bp.route('/register_new_book', methods=['GET', 'POST'])
@login_required
def register_new_book():
    """Register a new book and add it to the current user's collection."""
    form = BookForm()

    if form.validate_on_submit():
        try:
            # Generate shelf code from genre + author + title
            genre_title = form.genre.data.strip().title() if form.genre.data else 'General'
            code = generate_book_code(
                genre_title,
                form.author.data.strip(),
                form.title.data.strip()
            )

            if code is None:
                # Genre not in code_book dictionary — use fallback "000"
                author_initial = form.author.data.strip().split()[-1][0].upper()
                title_initial = form.title.data.strip()[0].lower()
                code = f'{author_initial}000{title_initial}'

            # Create the Book record
            book = Book(
                code=code,
                title=form.title.data.strip(),
                author=form.author.data.strip(),
                publisher=form.publisher.data.strip(),
                publication_year=form.year.data,
                pages=form.pages.data,
                genre=genre_title,
                isbn=form.isbn.data.strip() if form.isbn.data else None,
                cover_url=form.cover_url.data if form.cover_url.data else None,
            )

            db.session.add(book)
            db.session.flush()  # Get book.id

            # Create UserBooks link
            user_book = UserBooks(
                user_id=current_user.id,
                book_id=book.id,
                status=form.status.data or 'available',
                read_status=form.read.data or 'unread',
                format=form.format.data or 'physical',
                acquisition_date=datetime.utcnow()
            )
            db.session.add(user_book)
            db.session.commit()

            # Invalidate collection cache so new book appears immediately
            cache.clear()

            flash(f'"{book.title}" by {book.author} added to your collection! (Code: {book.code})', 'success')
            current_app.logger.info(
                f"Book {book.id} ('{book.title}') registered by user {current_user.id}, code={book.code}"
            )
            return redirect(url_for('books.your_collection'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error registering book: {str(e)}")
            flash(f'Error registering book: {str(e)}', 'danger')

    elif request.method == 'POST':
        # Form validation failed
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'warning')

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
        # Search filters: title (starts with), author (contains), ISBN (contains)
        search_filters = [
            Book.title.ilike(f'{query}%'),      # ← Starts with (better results)
            Book.author.ilike(f'%{query}%'),    # ← Contains (author names vary)
        ]
        # Add ISBN search if query looks like a number
        if query.replace('-', '').replace(' ', '').isdigit():
            search_filters.append(Book.isbn.ilike(f'%{query}%'))  # ← Contains (formatting variations)

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


@books_bp.route('/api/genres', methods=['GET'])
@login_required
@cache.cached(timeout=600)
def api_genres():
    """
    Return all available genres with their shelf codes (000–999),
    sorted numerically by code. Also returns custom user genres.
    """
    try:
        from app.models.code_book import book_genres

        # Build list sorted by code (numerically), skip empty names
        genre_list = [
            {'code': code, 'name': name}
            for code, name in sorted(book_genres.items(), key=lambda x: x[0])
            if name.strip()
        ]

        # Get custom genres from user's books that aren't in the master list
        master_names = {item['name'] for item in genre_list}
        user_genres = db.session.query(db.distinct(Book.genre)).join(
            UserBooks
        ).filter(
            UserBooks.user_id == current_user.id,
            Book.genre.isnot(None)
        ).all()
        user_genre_set = {g[0] for g in user_genres if g[0]}
        custom_genres = sorted(user_genre_set - master_names)

        return jsonify({
            'genres': genre_list,
            'custom': custom_genres,
            'default': 'General',
            'default_code': '000'
        })
    except Exception as e:
        current_app.logger.error(f"Genres API error: {e}")
        return jsonify({
            'genres': [{'code': '000', 'name': 'General'}],
            'custom': [],
            'default': 'General',
            'default_code': '000'
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

