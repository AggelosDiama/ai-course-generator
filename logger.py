import logging
import sys

def get_logger(name):
    logger = logging.getLogger(name)
    
    # Only configure if the logger doesn't have handlers already
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Format: Time - Agent Name - Level - Message
        formatter = logging.Formatter(
            '%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )

        # Stream Handler (Terminal)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        # File Handler (Log file)
        fh = logging.FileHandler('course_architect.log')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger