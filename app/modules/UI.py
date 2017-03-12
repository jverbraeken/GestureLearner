# coding=utf-8
import tkinter

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
        frame_main = tkinter.Frame(root)  # FrameMain(root, self.service_locator)
        self.service_locator.ui_bridge.add_button(frame_main, STRING_NEW_SAMPLE, self.create_new_sample)
        self.service_locator.ui_bridge.add_button(frame_main, STRING_SAVE, self.save)
        frame_main.pack()
        root.mainloop()

    def create_new_sample(self):
        """
        Create a new gesture sample
        """
        self.writer.add_class("foo")
        self.writer.add_sample("foo", [(1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12)])

    def save(self):
        self.writer.write_to_file("D:/UnrealProjects/foo.txt")
