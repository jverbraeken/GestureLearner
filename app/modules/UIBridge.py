# coding=utf-8
import uuid
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


def register(service_locator):
    UIBridge.service_locator = service_locator
    service_locator.ui_bridge = UIBridge()


class UIBridge:
    service_locator = None
    tree = None
    item = None
    entry = None

    def create_window(self):
        return Tk()

    def add_button(self, frame, text_in, command_in):
        button = Button(frame, text=text_in, comman=command_in)
        button.pack()
        return button

    def add_textbox(self, frame):
        self.entry = Entry(frame, width=20)
        self.entry.pack()
        return self.entry

    def create_tree(self, parent):
        self.tree = ttk.Treeview(parent)
        self.tree.heading('#0', text='Gestures')
        self.tree.pack()

    def add_gesture(self):
        if self.entry.get()!='':
            self.tree.insert('', 'end', uuid.uuid4(), text=self.entry.get())
            self.entry.delete(0, 'end')
            return self.entry.get()

    def add_sample(self):
        if self.entry.get()!='':
            item = self.tree.focus()
            if item!='':
                child = self.tree.insert(item, 'end', text=self.entry.get())
                self.entry.delete(0, 'end')
                return self.entry.get()


    def set_window_size(self, frame, width, height, x=300, y=300):
        frame.geometry(str(width) + "x" + str(height) + "+" + str(x) + "+" + str(y))

    def show_save_dialog(self, parent, title, initial_directory, file_types, default_extension):
        return filedialog.asksaveasfilename(parent=parent, defaultextension=default_extension,
                                            initialdir=initial_directory, title=title, filetypes=file_types)

    def show_open_dialog(self, parent, title, initial_directory, file_types, default_extension):
        return filedialog.askopenfilename(parent=parent, defaultextension=default_extension,
                                          initialdir=initial_directory, title=title, filetypes=file_types)
