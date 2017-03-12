# coding=utf-8
import tkinter

from app.modules.FrameMain import FrameMain

STRING_NEW_SAMPLE = "New Sample"
STRING_SAVE = "Save"


class UI:
    service_locator = None
    writer = None

    def init(self, service_locator):
        """
        Initialize the UI
        """
        self.service_locator = service_locator
        self.writer = service_locator.grt_writer
        root = self.service_locator.ui_bridge.create_window()
        frame_main = FrameMain(root, self.service_locator)
        frame_main.pack()
        root.mainloop()