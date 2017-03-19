# coding=utf-8
import uuid
from tkinter import *
from tkinter import ttk, filedialog, messagebox


def register(service_locator):
    UIBridge.service_locator = service_locator
    service_locator.ui_bridge = UIBridge()


class UIBridge:
    service_locator = None

    # Window

    def set_window_size(self, frame, width, height, x=300, y=300):
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
        tree = ttk.Treeview(parent)
        tree.pack()
        return tree

    def add_to_tree(self, tree, text, parent):
        return tree.insert(parent, 'end', uuid.uuid4(), text=text)

    def tree_focus(self, tree):
        return tree.focus()

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
