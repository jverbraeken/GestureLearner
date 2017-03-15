# coding=utf-8
from tkinter import *
from tkinter import filedialog


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

    def show_save_dialog(self, parent, title, initial_directory, file_types, default_extension):
        return filedialog.asksaveasfilename(parent=parent, defaultextension=default_extension,
                                            initialdir=initial_directory, title=title, filetypes=file_types)


    def show_open_dialog(self, parent, title, initial_directory, file_types, default_extension):
        return filedialog.askopenasfilename(parent=parent, defaultextension=default_extension,
                                            initialdir=initial_directory, title=title, filetypes=file_types)