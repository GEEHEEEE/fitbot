import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger('fitness_bot')
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s'
    )

    file_handler = RotatingFileHandler(
        'bot.log', maxBytes=5*1024*1024, backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger