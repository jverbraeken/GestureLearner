# coding=utf-8
from app.modules import UIBridge, GRTWriter


class ServiceLocator:
    grt_writer = None
    ui_bridge = None

    def __init__(self):
        self.init()

    def init(self):
        self.register_grt_writer()
        self.register_ui_bridge()

    def register_grt_writer(self):
        GRTWriter.register(self)

    def register_ui_bridge(self):
        UIBridge.register(self)
