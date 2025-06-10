import logging


class Logger:
    def __init__(self):
        self.app_logger = logging.getLogger("carbon")
        self.app_logger.setLevel(logging.INFO)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)

        self.formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        self.console_handler.setFormatter(self.formatter)

        self.app_logger.addHandler(self.console_handler)