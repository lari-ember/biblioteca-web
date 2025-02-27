# config.py
import os
from datetime import timedelta

# Configurações básicas
SECRET_KEY = os.getenv('SECRET_KEY', 'AmberlyqueriaS3erohalo')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:V0lBaT3rComAcaraNoposte@db:5432/biblioteca')
SQLALCHEMY_TRACK_MODIFICATIONS = False

CSRF_ENABLED = True
SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
REMEMBER_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # Tempo de sessão

# Configurações de logging
LOG_LEVEL = 'INFO'
LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'default'
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
}