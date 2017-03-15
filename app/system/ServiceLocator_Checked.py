# coding=utf-8
from app.modules.logging import Loggers
from app.system.ServiceLocator import ServiceLocator


class ServiceLocator_Checked(ServiceLocator):

    def __init__(self):
        ServiceLocator.__init__(self)

    def register_loggers(self):
        Loggers.register(self, False)
