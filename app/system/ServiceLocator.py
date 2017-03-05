from app.modules import UI, GRTWriter


class ServiceLocator:
    grt_writer = None
    ui = None

    def __init__(self, parent):
        self.init(parent)

    def init(self, parent):
        GRTWriter.register(self)
        UI.register(self, parent)
