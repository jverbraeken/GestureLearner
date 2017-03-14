# coding=utf-8
import logging

from app.modules.logging import LoggerLevels
from app.system import Constants


class Loggertje:
    name = ""
    logger = None

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(Constants.LOG_FILE + " - " + name + ".log")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def always(self, message):
        self.logger.critical(message)

    def error_always(self, message):
        self.logger.error(message)

    def warning_always(self, message):
        self.logger.warning(message)

    def user_input(self, message):
        self.logger.info("User input: " + message)

    def user_input_response(self, message):
        self.logger.info("Use input response: " + message)

    def error(self, message):
        if Constants.LOG_LEVEL >= LoggerLevels.error:
            self.logger.error(message)

    def warning(self, message):
        if Constants.LOG_LEVEL >= LoggerLevels.warning:
            self.logger.warning(message)

    def message(self, message):
        if Constants.LOG_LEVEL >= LoggerLevels.message:
            self.logger.info(message)

    def comment(self, message):
        if Constants.LOG_LEVEL >= LoggerLevels.comment:
            self.logger.debug(message)
