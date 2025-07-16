# __init__.py
import os
import time
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from sqlalchemy.exc import OperationalError
from flask_wtf import CSRFProtect

from .security.middleware import security_headers

# Inicializa extensões globais
db = SQLAlchemy()
cache = Cache()
login_manager = LoginManager()
csrf = CSRFProtect()

def configure_logging(app):
    """Configura o sistema de logging, gravando em arquivo e em stdout."""
    handler = RotatingFileHandler(
        'app.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Remova handlers antigos se existirem, para evitar duplicação
    # (opcional, dependendo do seu setup)
    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.addHandler(stream_handler)

    if app.config.get('DEBUG'):
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

def wait_for_db(app, retries=10, delay=2):
    """Tenta conectar ao banco repetidamente até sucesso ou esgotar retries."""
    with app.app_context():
        for attempt in range(1, retries + 1):
            try:
                # Consulta simples para verificar disponibilidade
                db.session.execute('SELECT 1')
                print("Banco disponível após %d tentativa(s)")
                app.logger.info("Banco disponível após %d tentativa(s)", attempt)
                return True
            except OperationalError as e:
                app.logger.warning("Tentativa %d falhou ao conectar ao banco: %s", attempt, e)
                time.sleep(delay)
        app.logger.error("Não conseguiu conectar ao banco após %d tentativas", retries)
        return False

def register_login_manager(app):
    """Configura o Flask-Login usando a instância global."""
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.modelsdb import User
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            app.logger.warning("load_user: Invalid user_id %s", user_id)
            return None
        except Exception as e:
            app.logger.error("load_user: Unexpected error for user_id %s: %s", user_id, str(e))
            return None

def register_blueprints(app):
    """Registra todos os blueprints da aplicação."""
    from app.controllers.auth import auth_bp
    from app.controllers.books import books_bp
    from app.controllers.routes import core_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(core_bp)

def create_app():
    """Factory function para criação da aplicação Flask."""
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    # Ajuste de proxy (se estiver atrás de proxy/reverse proxy)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=4, x_proto=4, x_host=4, x_prefix=4)

    # Configurações via variáveis de ambiente (evita hardcode em produção)
    secret = os.environ.get('SECRET_KEY')
    if not secret:
        app.logger.warning("SECRET_KEY não definido; usando fallback (apenas dev).")
        secret = 'dev-secret-key-fallback'
    app.config['SECRET_KEY'] = secret

    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        app.logger.warning("DATABASE_URL não definido; usando fallback (apenas dev).")
        database_url = 'postgresql://postgres:senha_dev@db:5432/biblioteca'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Carregar configurações adicionais de arquivo, se existir.
    # Cuidado: config.py não deve sobrescrever SECRET_KEY nem DATABASE_URL inadvertidamente.
    # Se usar config.py, garanta que ele leia variáveis de ambiente ou defina apenas parâmetros não-sensíveis.
    config_path = os.path.join(app.instance_path, '..', 'config.py')
    # Opcional: só carregar se existir:
    try:
        app.config.from_pyfile('../config.py')
    except FileNotFoundError:
        app.logger.info("config.py não encontrado; pulando load desse arquivo.")
    except Exception as e:
        app.logger.warning("Erro ao carregar config.py: %s", e)

    # Configura sessão/CSRF em desenvolvimento
    # Em produção, SESSION_COOKIE_SECURE idealmente True se usar HTTPS.
    if app.config.get('FLASK_ENV') == 'development':
        app.config['SESSION_COOKIE_SECURE'] = False
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    else:
        # Exemplo: em prod, se usar HTTPS:
        app.config.setdefault('SESSION_COOKIE_SECURE', True)
        app.config.setdefault('SESSION_COOKIE_SAMESITE', 'Lax')
    # Opcional: aumentar tempo de vida da sessão
    # app.config['PERMANENT_SESSION_LIFETIME'] = 3600

    # Setup logging
    configure_logging(app)

    # Registrar extensões
    db.init_app(app)
    csrf.init_app(app)
    register_login_manager(app)
    cache.init_app(app)

    # Registrar blueprints
    register_blueprints(app)

    # Aplica security headers após request
    app.after_request(security_headers)

    # Health check route
    @app.route('/health')
    def health_check():
        return 'OK', 200

    # Em ambiente de desenvolvimento, criar tabelas após banco disponível
    if app.config.get('FLASK_ENV') == 'development':
        print('asaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        app.logger.info("Ambiente de desenvolvimento: aguardando banco e criando tabelas se necessário.")
        if wait_for_db(app):
            with app.app_context():
                try:
                    db.create_all()
                    app.logger.info("db.create_all() executado com sucesso.")
                except Exception as e:
                    app.logger.error("Erro ao executar db.create_all(): %s", e)
        else:
            app.logger.error("Não foi possível conectar ao banco para criar tabelas em dev.")

    return app

# Cria a app
app = create_app()

# Importação de modelos (apenas para registrar no ORM); mantida após create_app
from app.models.modelsdb import User, Book, UserBooks, UserReadings, Loan, UserRead
with app.app_context():
    db.create_all()