import sys
import logging
from logging import handlers
import os

# Setup a logger (writes to file and console)
logger = logging.getLogger("mlproject_logger")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Log to file
log_file = os.path.join(os.path.dirname(__file__), "mlproject.log")
file_handler = handlers.RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(formatter)

# Log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def error_message_detail(error, error_detail):
    """Extract filename, line number, and format error message."""
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    return f"Error occurred in python script [{file_name}] line number [{exc_tb.tb_lineno}] error message [{error}]"


class CustomException(Exception):
    """Custom Exception that logs itself automatically."""
    def __init__(self, error_message, error_detail):
        self.error_message = error_message_detail(error_message, error_detail)
        logger.error(self.error_message)  # Automatically log the error
        super().__init__(self.error_message)


