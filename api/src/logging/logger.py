import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

class Logger:
    def __init__(self, name=__name__, level=logging.INFO, log_dir="logs"):
        """
        Initialize the logger and setup the basic configurations
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Log file path
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

        # Create handlers
        file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """
        Return the logger instance
        """
        return self.logger
