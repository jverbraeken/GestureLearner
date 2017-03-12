# coding=utf-8
from tkinter import *


def register(service_locator):
    UIBridge.service_locator = service_locator
    service_locator.ui_bridge = UIBridge()


class UIBridge:
    service_locator = None

    def create_window(self):
        return Tk()

    def add_button(self, frame, text_in, command_in):
        button = Button(frame, text=text_in, comman=command_in)
        button.pack()
        return button

    def set_window_size(self, frame, width, height, x=300, y=300):
        frame.geometry(str(width) + "x" + str(height) + "+" + str(x) + "+" + str(y))