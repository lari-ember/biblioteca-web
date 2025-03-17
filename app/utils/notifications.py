from datetime import datetime


def format_success_message(book):
    """Formata mensagem de sucesso com detalhes do livro."""
    return {
        'category': 'success',
        'title': '📚 Book Registered!',
        'html': f"""
            <div class="alert-content">
                <h4>{book.title}</h4>
                <ul class="book-details">
                    <li>Author: {book.author}</li>
                    <li>Code: <code>{book.code}</code></li>
                    <li>Added: {datetime.now().strftime('%Y-%m-%d %H:%M')}</li>
                </ul>
            </div>
        """
    }