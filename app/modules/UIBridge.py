# coding=utf-8
import uuid
from tkinter import *
from tkinter import ttk, filedialog, messagebox

from app.system import Constants


def register(service_locator):
    UIBridge.service_locator = service_locator
    service_locator.ui_bridge = UIBridge()


class UIBridge:
    service_locator = None

    # Window

    def set_window_size(self, frame, width, height, x=100, y=100):
        frame.geometry(str(width) + "x" + str(height) + "+" + str(x) + "+" + str(y))

    def create_window(self):
        return Tk()

    # Button

    def add_button(self, frame, text_in, command_in):
        button = Button(frame, text=text_in, comman=command_in)
        button.pack()
        return button

    # Textbox

    def add_textbox(self, frame):
        entry = Entry(frame, width=20)
        entry.pack()
        return entry

    def get_textbox_string(self, textbox):
        return textbox.get()

    def clear_textbox(self, textbox):
        textbox.delete(0, "end")

    # Tree

    def add_tree(self, parent):
        frame = Frame(parent)
        frame.pack(side=TOP)
        scroll = ttk.Scrollbar(frame, orient=VERTICAL)
        tree = ttk.Treeview(frame, yscrollcommand=scroll.set)
        tree.heading('#0', text='Gestures')
        tree.column("#0", minwidth=0, width=int(Constants.WIDTH * 0.9), stretch=NO)
        scroll.configure(command=tree.yview)
        tree.pack(expand=YES, side=LEFT, fill=BOTH)
        scroll.pack(side=RIGHT, fill=Y)
        return tree

    def add_to_tree(self, tree, text, parent, uuid_in=None):
        if uuid_in is None:
            uuid_in = uuid.uuid4()
        return tree.insert(parent, 'end', uuid_in, text=text)

    def delete_from_tree(self, tree, uuid_in):
        tree.delete(uuid_in)

    def tree_focus(self, tree):
        return tree.focus()

    def tree_clear(self, tree):
        tree.delete(*tree.get_children())

    # Dialogs

    def show_error(self, text):
        messagebox.showerror("Error", text)

    def show_warning(self, text):
        messagebox.showwarning("Warning", text)

    def show_info(self, text):
        messagebox.showinfo("Information", text)

    def ask_question(self, text):
        return messagebox.askquestion("Question", text)

    # Window Dialogs

    def show_save_dialog(self, parent, title, initial_directory, file_types, default_extension):
        return filedialog.asksaveasfilename(parent=parent, defaultextension=default_extension,
                                            initialdir=initial_directory, title=title, filetypes=file_types)

    def show_open_dialog(self, parent, title, initial_directory, file_types, default_extension):
        return filedialog.askopenfilename(parent=parent, defaultextension=default_extension,
                                          initialdir=initial_directory, title=title, filetypes=file_types)
