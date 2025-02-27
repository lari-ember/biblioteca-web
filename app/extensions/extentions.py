# app/extensions.py
from functools import wraps

from flask import redirect, url_for, request, session, abort
from flask_login import LoginManager

login_manager = LoginManager()


def init_login_manager(app):
    login_manager.init_app(app)

    # Configurações de segurança
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = "strong"
    login_manager.needs_refresh_message = (u"Sessão expirada, faça login novamente")
    login_manager.needs_refresh_message_category = "info"

    # Configuração para carregamento tardio do user_loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.modelsdb import User  # Importação tardia para evitar circular
        return User.query.get(int(user_id))

    # Configuração de callback para requisições não autorizadas
    @login_manager.unauthorized_handler
    def handle_needs_login():
        return redirect(url_for('auth.login', next=request.endpoint))

    # Habilitar proteção CSRF para login
    def csrf_protect(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == "POST":
                csrf_token = session.pop('_csrf_token', None)
                if not csrf_token or csrf_token != request.form.get('_csrf_token'):
                    abort(403)
            return f(*args, **kwargs)

        return decorated_function

    login_manager.request_loader(csrf_protect)