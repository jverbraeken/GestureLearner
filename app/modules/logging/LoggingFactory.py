# coding=utf-8
import logging
import os

from app.modules.logging import Loggers
from app.modules.logging.Logger import Loggertje
from app.system import Constants


def register(service_locator):
    LoggingFactory.service_locator = service_locator
    service_locator.logger_factory = LoggingFactory()

class LoggingFactory:
    loggers = {}

    def __init__(self):
        if Constants.CLEAN_LOGS_ON_RESTART:
            for log in ["system", "udp_scanner", "ui", "grt_writer", "undefined"]:
                try:
                    os.remove(Constants.LOG_FILE + " - " + log + ".log")
                except OSError:
                    pass

    def get_logger(self, logger_id):
        if logger_id in self.loggers:
            return self.loggers[logger_id]
        else:
            name = Loggers.getLogNameFromID(logger_id)
            logger = Loggertje(name)
            self.loggers[logger_id] = logger
            return logger
