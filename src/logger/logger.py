import logging
import sys
import os

def get_logger(name):
    # 1. Get the path of the current file (logger.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(current_dir, "app.py.log")

    # 2. Create the logger
    logger = logging.getLogger(name)
    
    # Only configure if the logger doesn't have handlers already
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Create file handler
        file_handler = logging.FileHandler(log_file_path)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        # Create console handler (for your terminal)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(file_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger