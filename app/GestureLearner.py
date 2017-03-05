from tkinter import *

STRING_NEW_SAMPLE = "New Sample"


class GestureLearner(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        """
        Initialize the UI
        @return:
        @rtype:
        """
        self.parent.title("Gesture Learner")

        self.pack(fill=BOTH, expand=1)

        button_new_sample = Button(self, text=STRING_NEW_SAMPLE, command=self.create_new_sample)

        button_new_sample.pack()

    def create_new_sample(self):
        print("clicked!")
