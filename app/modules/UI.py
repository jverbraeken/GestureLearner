from tkinter import *

from app.modules.GRTWriter import GRTWriter

STRING_NEW_SAMPLE = "New Sample"
STRING_SAVE = "Save"


def register(service_locator, parent):
    UI.service_locator = service_locator
    service_locator.ui = UI(parent)


class UI(Frame):
    service_locator = None
    writer = None

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init()
        self.writer = self.service_locator.grt_writer

    def init(self):
        """
        Initialize the UI
        """
        self.parent.title("Gesture Learner")

        self.pack(fill=BOTH, expand=1)

        button_new_sample = Button(self, text=STRING_NEW_SAMPLE, command=self.create_new_sample)
        button_new_sample.pack()
        button_save = Button(self, text=STRING_SAVE, command=self.save)
        button_save.pack()

    def create_new_sample(self):
        """
        Create a new gesture sample
        """
        self.writer.add_class("foo")
        self.writer.add_sample("foo", [(1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12)])

    def save(self):
        self.writer.write_to_file("E:/Desktop/foo.grt")
