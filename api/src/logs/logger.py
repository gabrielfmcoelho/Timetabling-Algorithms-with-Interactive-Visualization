from datetime import datetime
from icecream import ic

import logging
import os


class Logger:
    logger_instance = None

    def __init__(self, name=__name__, level=logging.INFO, log_dir="logs"):
        """
        Initialize the logger and setup the basic configurations
        """
        if Logger.logger_instance is None:    
            ic(f"Initializing logger with name: {name}, level: {level}, log_dir: {log_dir}")
            iteration = len(self.list_logs_files()) + 1
            try:
                self.logger = logging.getLogger(name)
                self.logger.setLevel(level)

                # Create log directory if it doesn't exist
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)

                # Log file path
                log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}_{iteration}.log")

                # Create handlers
                file_handler = logging.handlers.TimedRotatingFileHandler(log_file, when="midnight", interval=1)
                file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
                
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

                # Add handlers to the logger
                self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)
                self.logger.info(f"Logger initialized with name: {name}, level: {level}, log_dir: {log_dir}")
            except Exception as e:
                ic(e)
                raise ValueError("Error initializing logger")
            Logger.logger_instance = self
        else:
            self.logger = Logger.logger_instance.logger
        
    def list_logs_files(self):
        """
        List the log files in the log directory
        """
        return os.listdir("logs/history")

    def get_logger(self):
        """
        Return the logger instance
        """
        return self.logger
