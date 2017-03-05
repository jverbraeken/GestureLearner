from app.modules import GRTWriter_Checked
from app.system.ServiceLocator import ServiceLocator


class ServiceLocator_Checked(ServiceLocator):
    def __init__(self):
        ServiceLocator.__init__(self)

    def init(self):
        ServiceLocator.init(self)
        GRTWriter_Checked.register(self)