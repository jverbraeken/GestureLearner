from tkinter import *

from app.GRTWriter import GRTWriter

STRING_NEW_SAMPLE = "New Sample"
STRING_SAVE = "Save"


class GestureLearner(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
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
        print("clicked!")

    def save(self):
        writer = GRTWriter("foo", "bar")
        writer.write_to_file("E:/Desktop/foo.grt")