import logging
import sys
from cor_auth.conf.config import settings
from logging.handlers import TimedRotatingFileHandler

DEBUG = settings.debug

logger = logging.getLogger(__name__)
if DEBUG:
        logger.setLevel(logging.DEBUG)
else:
        logger.setLevel(logging.INFO)

def handle_exception(exc_type, exc_value, exc_traceback):
    # Логирование информации об исключении
    logger.error("An unhandled exception occurred", exc_info=(exc_type, exc_value, exc_traceback))

# Регистрация обработчика исключений
sys.excepthook = handle_exception


file_handler = TimedRotatingFileHandler('logs.log', when='M', backupCount=7)
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s"))
logger.addHandler(file_handler)


stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)