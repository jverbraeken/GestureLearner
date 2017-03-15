# coding=utf-8
from app.modules.filesystem import GRTWriter_Checked
from app.modules.logging import Loggers
from app.system.ServiceLocator import ServiceLocator


class ServiceLocator_Checked(ServiceLocator):

    def __init__(self):
        ServiceLocator.__init__(self)

    def register_grt_writer(self):
        GRTWriter_Checked.register(self)

    def register_loggers(self):
        Loggers.register(self, False)
