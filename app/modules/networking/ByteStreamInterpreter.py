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
            (zrot,) = unpack_from('!f', byte_string, 1)
            (vx,) = unpack_from('!f', byte_string, 5)
            (vy,) = unpack_from('!f', byte_string, 9)
            (vz,) = unpack_from('!f', byte_string, 13)
            (ax,) = unpack_from('!f', byte_string, 17)
            (ay,) = unpack_from('!f', byte_string, 21)
            (az,) = unpack_from('!f', byte_string, 25)
            self.logger.user_input(
                "interpreted rotation: zrot = " + str(zrot)
                + ", vx = " + str(vx) + ", vy = " + str(vy) + ", vz = " + str(vz)
                + ", ax = " + str(ax) + ", ay = " + str(ay) + ", az = " + str(az))
            return zrot, (vx, vy, vz), (ax, ay, az)
        elif request == self.COMTP_SHAKING_STARTED:
            return -1
        elif request == self.COMTP_SHAKING_STOPED:
            return -1
