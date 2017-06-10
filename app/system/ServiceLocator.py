# coding=utf-8
from app.modules import UIBridge
from app.modules.data import Data
from app.modules.filesystem import GRTWriter, GRTReader
from app.modules.logging import Loggers, LoggerFactory
from app.modules.networking import UDPScanner, ByteStreamInterpreter
from app.modules.framing import Framer


class ServiceLocator:
    grt_reader = None
    grt_writer = None
    ui_bridge = None
    logger_factory = None
    udp_scanner = None
    byte_stream_interpreter = None
    data = None
    framer = None

    def __init__(self):
        self.init()

    def init(self):
        self.register_logging_factories()
        self.register_loggers()
        self.register_grt_reader()
        self.register_grt_writer()
        self.register_ui_bridge()
        self.register_udp_scanner()
        self.register_byte_stream_interpreter()
        self.register_data()
        self.register_framer()

    def register_logging_factories(self):
        LoggerFactory.register(self)

    def register_grt_reader(self):
        GRTReader.register(self)

    def register_grt_writer(self):
        GRTWriter.register(self)

    def register_ui_bridge(self):
        UIBridge.register(self)

    def register_loggers(self):
        Loggers.register(self, True)

    def register_udp_scanner(self):
        UDPScanner.register(self)

    def register_byte_stream_interpreter(self):
        ByteStreamInterpreter.register(self)

    def register_data(self):
        Data.register(self)

    def register_framer(self):
        Framer.register(self)