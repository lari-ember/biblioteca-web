from functools import wraps

from flask import request, current_app, Response, redirect


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