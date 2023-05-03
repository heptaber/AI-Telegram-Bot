"""
Logger implementation.
"""

#!/user/bin/python3


import logging
import os


class Logger:
    def __init__(self, filename, max_lines=1000):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

        self.max_lines = max_lines
        self.check_file_size()

    def info(self, message):
        self.logger.info(message)
        self.check_file_size()

    def warning(self, message):
        self.logger.warning(message)
        self.check_file_size()

    def error(self, message):
        self.logger.error(message)
        self.check_file_size()

    def check_file_size(self):
        try:
            with open(self.logger.handlers[0].baseFilename, 'r') as f:
                lines = f.readlines()
                if len(lines) >= self.max_lines:
                    with open(self.logger.handlers[0].baseFilename, 'w'):
                        pass
        except Exception as e:
            print(f"Error while checking file size: {e}")
