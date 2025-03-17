# app/extensions.py
from flask_login import LoginManager

def init_login_manager(app):
    """Inicializa o Flask-Login com configurações de segurança."""
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Rota de login
    login_manager.session_protection = "strong"  # Proteção de sessão

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.modelsdb import User  # Importação local para evitar circular imports
        return User.query.get(int(user_id))