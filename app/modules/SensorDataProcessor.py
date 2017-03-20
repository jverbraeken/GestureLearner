# coding=utf-8

def register(service_locator):
    SensorDataProcessor.service_locator = service_locator
    service_locator.sensor_data_processor = SensorDataProcessor(service_locator)


class SensorDataProcessor:
    service_locator = None
    listeners = []

    def __init__(self, service_locator):
        self.service_locator = service_locator

    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)

    def process_data(self, data):
        """
        Processes the incoming tuple. TODO: the data may not be a tuple!
        Args:
            data: a tuple containing a tuple for the rotation and a tuple for the acceleration

        Returns: -

        """
        for listener in self.listeners:
            listener.data_received(data[0][0], data[0][1], data[0][2], data[1][0], data[1][1], data[1][2])
