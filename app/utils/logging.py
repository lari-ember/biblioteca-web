import logging

from flask import request, current_app
from flask_login import current_user


def setup_logging(app):
    """Configuração centralizada de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
    app.logger = logging.getLogger(__name__)


def log_activity(message: str, level: str = 'info'):
    """Registro estruturado de atividades"""
    user_id = current_user.id if current_user.is_authenticated else 'anonymous'
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)

    log_data = {
        'user': user_id,
        'ip': ip_address,
        'endpoint': request.endpoint,
        'method': request.method,
        'user_agent': request.user_agent.string
    }

    logger = current_app.logger
    log_message = f"{message} | Metadata: {log_data}"

    if level.lower() == 'warning':
        logger.warning(log_message)
    elif level.lower() == 'error':
        logger.error(log_message)
    else:
        logger.info(log_message)