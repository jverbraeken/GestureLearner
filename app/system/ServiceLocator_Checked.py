# coding=utf-8
from app.modules import GRTWriter_Checked
from app.system.ServiceLocator import ServiceLocator


class ServiceLocator_Checked(ServiceLocator):
    grt_writer = None
    ui_bridge = None

    def __init__(self):
        ServiceLocator.__init__(self)

    def register_grt_writer(self):
        GRTWriter_Checked.register(self)
