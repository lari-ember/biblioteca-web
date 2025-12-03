from functools import wraps
from typing import Callable, Optional

from flask import request, current_app, Response, redirect, g, make_response, render_template


def security_headers(response: Response) -> Response:
    """Adiciona headers de segurança à resposta"""
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    #response.headers['X-Content-Type-Options'] = 'nosniff'
    #response.headers['X-Frame-Options'] = 'DENY'
    #response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


def require_https(f):
    """Força uso de HTTPS em produção"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_app.config.get('ENV') == 'production':
            if not request.is_secure:
                return redirect(request.url.replace('http://', 'https://'), code=301)
        return f(*args, **kwargs)
    return decorated_function


def seo_meta(
    title: Optional[Callable] = None,
    description: Optional[Callable] = None,
    image: Optional[Callable] = None,
    book_data: bool = False
):
    """
    Decorator for adding dynamic SEO metadata to routes.

    Injects Open Graph tags and other SEO metadata into the Flask `g` object
    for use in base.html template. Callbacks receive the route's return context.

    Args:
        title: Callable that returns og:title string
        description: Callable that returns og:description string
        image: Callable that returns og:image URL
        book_data: If True, expects book object in context for structured data

    Usage:
        @app.route('/view_book/<int:book_id>')
        @seo_meta(
            title=lambda ctx: ctx.get('book', {}).get('title', 'Book'),
            description=lambda ctx: ctx.get('book', {}).get('description', ''),
            image=lambda ctx: ctx.get('book', {}).get('cover_url'),
            book_data=True
        )
        def view_book(book_id):
            book = Book.query.get_or_404(book_id)
            return render_template('view_book.html', book=book)

    Template Integration:
        In base.html <head> section:
        {% if g.seo_metadata %}
          <meta property="og:title" content="{{ g.seo_metadata.title }}" />
          <meta property="og:description" content="{{ g.seo_metadata.description }}" />
          <meta property="og:image" content="{{ g.seo_metadata.image }}" />
          <meta property="og:type" content="{{ g.seo_metadata.type }}" />
        {% endif %}
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Execute the route function
            result = f(*args, **kwargs)

            # Extract context from result
            context = {}
            if isinstance(result, tuple):
                # Handle (rendered_template, status_code) tuple
                template_result = result[0]
                if hasattr(template_result, 'context'):
                    context = template_result.context
            elif isinstance(result, str):
                # String response, can't extract context
                pass
            elif hasattr(result, 'context'):
                # Direct template render
                context = result.context

            # Build SEO metadata
            seo_data = {
                'title': title(context) if title and callable(title) else current_app.config.get('SITE_NAME', 'Amber Archively'),
                'description': description(context) if description and callable(description) else 'Personal library management system',
                'image': image(context) if image and callable(image) else None,
                'type': 'book' if book_data else 'website',
                'url': request.url
            }

            # Store in Flask g object for template access
            g.seo_metadata = seo_data

            return result

        return decorated_function
    return decorator
