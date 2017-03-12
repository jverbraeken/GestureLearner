# coding=utf-8

from tkinter import Frame, BOTH

from app.modules.logging import Loggers
from app.system import Constants

STRING_NEW_SAMPLE = "New Sample"
STRING_SAVE = "Save"


class FrameMain(Frame):
    parent = None
    writer = None
    background = "white"
    service_locator = None
    logger = None

    def __init__(self, parent, service_locator):
        Frame.__init__(self, parent)

        self.service_locator = service_locator
        self.writer = self.service_locator.grt_writer

        self.parent = parent
        self.parent.title(Constants.APPLICATION_NAME)
        self.pack(fill=BOTH, expand=1)
        self.service_locator.ui_bridge.set_window_size(parent, Constants.WIDTH, Constants.HEIGHT)

        self.service_locator.ui_bridge.add_button(parent, STRING_NEW_SAMPLE, self.create_new_sample)
        self.service_locator.ui_bridge.add_button(parent, STRING_SAVE, self.save)

        self.logger = self.service_locator.logger_factory.get_logger(Loggers.ui)

        self.service_locator.udp_scanner.start_listening("0.0.0.0", 55056)

    def create_new_sample(self):
        """
        Create a new gesture sample
        """
        self.logger.user_input("Button pressed: create_new_sample")
        self.writer.add_class("foo")
        self.writer.add_sample("foo", [(1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12)])

    def save(self):
        self.writer.write_to_file("C:/Users/Public/foo.grt")
