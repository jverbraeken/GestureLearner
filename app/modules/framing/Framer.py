# coding=utf-8

def register(service_locator):
    Framer.service_locator = service_locator
    service_locator.framer = Framer()


class Framer:
    service_locator = None

    def getCaptures(self):
        pass