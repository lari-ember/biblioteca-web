# __init__.py
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

# Inicializa extensões
db = SQLAlchemy()
lm = LoginManager()


def create_app():
    """Factory function para criação da aplicação Flask"""
    app = Flask(__name__)

    # Configurações básicas
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=4, x_proto=4, x_host=4, x_prefix=4
    )

    # Carrega configurações
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config.from_pyfile('config.py')

    # Configuração de logging
    configure_logging(app)

    # Inicialização ordenada
    db.init_app(app)
    lm.init_app(app)
    lm.login_view = 'auth.login'
    lm.session_protection = "strong"
    register_blueprints(app)
    from extensions import init_login_manager
    init_login_manager(app)  # Agora com CSRF e segurança reforçada

    # Garantir que os modelos são carregados antes de qualquer operação com o DB
    with app.app_context():
        db.create_all()

    return app


def configure_logging(app):
    """Configura o sistema de logging"""
    handler = RotatingFileHandler(
        'app.log',
        maxBytes=1024 * 1024 * 10,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Define nível de log baseado no ambiente
    if app.config['DEBUG']:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)


def register_blueprints(app):
    """Registra todos os blueprints da aplicação"""
    from app.controllers.auth import auth_bp
    from app.controllers.books import books_bp
    from app.controllers.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(main_bp)

# Importação de modelos deve ser feita após a criação do db
from app.models.modelsdb import User, Book, UserBooks, UserReadings, Loan, UserRead

app = create_app()