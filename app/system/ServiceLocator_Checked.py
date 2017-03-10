from app.modules import GRTWriter_Checked
from app.system.ServiceLocator import ServiceLocator


class ServiceLocator_Checked(ServiceLocator):
    grt_writer = None
    ui = None

    def __init__(self, parent):
        ServiceLocator.__init__(self, parent)

    def register_grt_writer(self):
        GRTWriter_Checked.register(self)
