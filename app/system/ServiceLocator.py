from app.modules import UI, GRTWriter


class ServiceLocator:
    def __init__(self):
        self.ui = None
        self.grt_writer = None
        self.init()

    def init(self):
        UI.register(self)
        GRTWriter.register(self)
