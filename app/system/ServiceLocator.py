# coding=utf-8
from app.modules import UIBridge, GRTWriter
from app.modules.logging import Loggers
from app.modules.logging import LoggingFactory


class ServiceLocator:
    grt_writer = None
    ui_bridge = None
    logger_factory = None
    udp_scanner = None

    def __init__(self):
        self.init()

    def init(self):
        self.register_logging_factories()
        self.register_loggers()
        self.register_grt_writer()
        self.register_ui_bridge()

    def register_logging_factories(self):
        LoggingFactory.register(self)

    def register_grt_writer(self):
        GRTWriter.register(self)

    def register_ui_bridge(self):
        UIBridge.register(self)

    def register_loggers(self):
        Loggers.register(self, True)
