from app.modules import UI, GRTWriter


class ServiceLocator:
    grt_writer = None
    ui = None

    def __init__(self, parent):
        self.init(parent)

    def init(self, parent):
        self.register_grt_writer()
        self.register_ui(parent)

    def register_grt_writer(self):
        GRTWriter.register(self)

    def register_ui(self, parent):
        UI.register(self, parent)
