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

    def interpret_rot_acc(self, byte_string):
        (rx,) = unpack_from('!f', byte_string, 0)
        (ry,) = unpack_from('!f', byte_string, 4)
        (rz,) = unpack_from('!f', byte_string, 8)
        (ax,) = unpack_from('!f', byte_string, 12)
        (ay,) = unpack_from('!f', byte_string, 14)
        (az,) = unpack_from('!f', byte_string, 16)
        self.logger.user_input("interpreted rotation: x = " + str(rx) + ", y = " + str(ry) + ", z = " + str(
            rz) + " / acceleration: x = " + str(ax) + ", y = " + str(ay) + ", z = " + str(az))
        return (rx, ry, rz), (ax, ay, az)
