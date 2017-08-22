# coding=utf-8
from struct import unpack_from

from app.modules.logging import Loggers


def register(service_locator):
    ByteStreamInterpreter.service_locator = service_locator
    service_locator.byte_stream_interpreter = ByteStreamInterpreter(service_locator)


class ByteStreamInterpreter:
    COMTP_SENSOR_DATA = 1
    COMTP_SHAKING_STARTED = 2
    COMTP_SHAKING_STOPED = 3

    service_locator = None

    def __init__(self, service_locator):
        self.service_locator = service_locator
        self.logger = service_locator.logger_factory.get_logger(Loggers.byte_stream_interpreter)

    def interpret_data(self, byte_string):
        (request,) = unpack_from('!B', byte_string, 0)
        if request == self.COMTP_SENSOR_DATA:
            (rx,) = unpack_from('!f', byte_string, 1)
            (ry,) = unpack_from('!f', byte_string, 5)
            (rz,) = unpack_from('!f', byte_string, 9)
            (rtime,) = unpack_from('!q', byte_string, 13)
            (ax,) = unpack_from('!f', byte_string, 21)
            (ay,) = unpack_from('!f', byte_string, 25)
            (az,) = unpack_from('!f', byte_string, 29)
            self.logger.user_input(
                "interpreted rotation: rx = " + str(rx) + ", ry = " + str(ry) + ", rz = " + str(rz) + ", rtime = " + str(rtime)
                + ", ax = " + str(ax) + ", ay = " + str(ay) + ", az = " + str(az))
            return (rx, ry, rz), (ax, ay, az), (rtime)
        elif request == self.COMTP_SHAKING_STARTED:
            return -1
        elif request == self.COMTP_SHAKING_STOPED:
            return -1
