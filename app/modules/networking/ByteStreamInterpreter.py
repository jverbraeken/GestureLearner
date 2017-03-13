# coding=utf-8
from struct import unpack_from

from app.modules.logging import Loggers


def register(service_locator):
    ByteStreamInterpreter.service_locator = service_locator
    service_locator.byte_stream_interpreter = ByteStreamInterpreter(service_locator)


class ByteStreamInterpreter:
    service_locator = None

    def __init__(self, service_locator):
        self.service_locator = service_locator
        self.logger = service_locator.logger_factory.get_logger(Loggers.byte_stream_interpreter)

    def interpret_rotation(self, byte_string):
        (x,) = unpack_from('!f', byte_string, 0)
        (y,) = unpack_from('!f', byte_string, 4)
        (z,) = unpack_from('!f', byte_string, 8)
        self.logger.user_input("interpreted rotation: x = " + str(x) + ", y = " + str(y) + ", z = " + str(z))
        return x, y, z
