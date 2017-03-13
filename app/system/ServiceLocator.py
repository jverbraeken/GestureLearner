# coding=utf-8
from app.modules import Data
from app.modules import SensorDataProcessor
from app.modules import UIBridge, GRTWriter
from app.modules.logging import Loggers, LoggerFactory
from app.modules.networking import UDPScanner, ByteStreamInterpreter


class ServiceLocator:
    grt_writer = None
    ui_bridge = None
    logger_factory = None
    udp_scanner = None
    byte_stream_interpreter = None
    sensor_data_processor = None
    data = None

    def __init__(self):
        self.init()

    def init(self):
        self.register_logging_factories()
        self.register_loggers()
        self.register_grt_writer()
        self.register_ui_bridge()
        self.register_udp_scanner()
        self.register_byte_stream_interpreter()
        self.register_sensor_data_processor()
        self.register_data()

    def register_logging_factories(self):
        LoggerFactory.register(self)

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

    def register_sensor_data_processor(self):
        SensorDataProcessor.register(self)

    def register_data(self):
        Data.register(self)
