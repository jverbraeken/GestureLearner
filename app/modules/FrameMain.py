# coding=utf-8
from tkinter import Frame, BOTH

from app.modules.data import DataLayers
from app.modules.logging import Loggers
from app.system import Constants

STRING_NEW_GESTURE = "New Gesture"
STRING_NEW_SAMPLE = "New Sample"
STRING_NEW_TIME_STATE = "New Time State"
STRING_OPEN = "Open"
STRING_SAVE = "Save"
STRING_EXPORT = "Export"
STRING_START_RECORDING = "Start Recording"
STRING_STOP_RECORDING = "Stop Recording"
STRING_OPEN_DIALOG = "Choose the grt or grtraw file you want to open"
STRING_SAVE_DIALOG = "Choose where you want to save the GRT data"


class FrameMain(Frame):
    parent = None
    writer = None
    background = "white"
    sL = None
    logger = None
    ui = None

    # UI
    textbox = None
    tree = None

    selected_gesture = None
    selected_sample = None
    selected_time_state = None


    def __init__(self, parent, service_locator):
        Frame.__init__(self, parent)

        self.sL = service_locator
        self.logger = self.sL.logger_factory.get_logger(Loggers.ui)
        self.ui = self.sL.ui_bridge
        self.writer = self.sL.grt_writer
        self.reader = self.sL.grt_reader

        self.parent = parent
        self.parent.title(Constants.APPLICATION_NAME)
        self.pack(fill=BOTH, expand=1)
        self.ui.set_window_size(parent, Constants.WIDTH, Constants.HEIGHT)

        self.tree = self.ui.add_tree(parent)
        self.textbox = self.ui.add_textbox(parent)
        self.ui.add_button(parent, STRING_NEW_GESTURE, self.create_new_gesture)
        self.ui.add_button(parent, STRING_NEW_SAMPLE, self.create_new_sample)
        self.ui.add_button(parent, STRING_NEW_TIME_STATE, self.create_new_time_state)
        self.ui.add_button(parent, STRING_OPEN, self.open)
        self.ui.add_button(parent, STRING_SAVE, self.save)
        self.ui.add_button(parent, STRING_EXPORT, self.export)
        self.ui.add_button(parent, STRING_START_RECORDING, self.start_recording)
        self.ui.add_button(parent, STRING_STOP_RECORDING, self.stop_recording)

    def create_new_gesture(self):
        """
        Create a new gesture
        """
        self.logger.user_input("Button pressed: create_new_gesture")
        self.update_selected()
        name = self.ui.get_textbox_string(self.textbox)
        if name is "":
            self.ui.show_error("Please enter a valid name")
            self.logger.message("create_new_gesture aborted - no name entered")
            return
        uuid = self.ui.add_to_tree(self.tree, name, "")
        self.ui.clear_textbox(self.textbox)
        self.sL.data.add_gesture(name, uuid)

    def create_new_sample(self):
        """
        Create a new gesture sample
        """
        self.logger.user_input("Button pressed: create_new_sample")
        self.update_selected()
        if not self.selected_gesture:
            self.ui.show_error("Please select a gesture first")
            self.logger.message("create_new_sample aborted - no gesture selected")
            return
        name = self.ui.get_textbox_string(self.textbox)
        if name is "":
            self.ui.show_error("Please enter a valid name")
            self.logger.message("create_new_sample aborted - no name entered")
            return
        uuid = self.ui.add_to_tree(self.tree, name, self.selected_gesture)
        self.ui.clear_textbox(self.textbox)
        self.sL.data.add_sample(name, uuid, self.sL.data.uuid_dict[self.selected_gesture][1])

    def create_new_time_state(self):
        """
        Create a new gesture sample time state (rotation / acceleration)
        """
        self.logger.user_input("Button pressed: create_new_time_state")
        self.update_selected()
        if not self.selected_sample:
            self.ui.show_error("Please select a sample first")
            self.logger.message("create_new_time_state aborted - no sample selected")
            return
        rotation_tuple = (0, 1, 2)
        acceleration_tuple = (3, 4, 5)
        if rotation_tuple is not None and acceleration_tuple is not None:
            uuid = self.ui.add_to_tree(self.tree, "rot: " + str(rotation_tuple) + " / acc: " + str(acceleration_tuple),
                                       self.selected_sample)
            self.sL.data.add_time_state(uuid, self.sL.data.uuid_dict[str(self.selected_sample)][1])

    def save(self):
        path = self.ui.show_save_dialog(
            parent=self.parent,
            title=STRING_SAVE_DIALOG,
            initial_directory=Constants.INITIAL_SAVE_DIRECTORY,
            file_types=[("Raw Gesture Recognition Toolkit files", ".grtraw")],
            default_extension=".grtraw")
        if path != "":
            self.writer.write_grt(path)

    def export(self):
        path = self.ui.show_save_dialog(
            parent=self.parent,
            title=STRING_SAVE_DIALOG,
            initial_directory=Constants.INITIAL_SAVE_DIRECTORY,
            file_types=[("Gesture Recognition Toolkit files", ".grt")],
            default_extension=".grt")
        if path != "":
            self.writer.write_grtraw(path)

    def open(self):
        path = self.ui.show_open_dialog(
            parent=self.parent,
            title=STRING_OPEN_DIALOG,
            initial_directory=Constants.INITIAL_SAVE_DIRECTORY,
            file_types=[("Raw Gesture Recognition Toolkit files", ".grtraw"),
                        ("Gesture Recognition Toolkit files", ".grt")],
            default_extension=".grtraw")
        if path != "":
            self.sL.data = self.reader.read_file(path)
            self.reload_treeview()

    def start_recording(self):
        data = self.sL.data
        data.gestures[data.selected_gesture].add_sample()
        self.sL.udp_scanner.start_listening("0.0.0.0", 55056, self.redirect_raw_recording)

    def stop_recording(self):
        self.sL.udp_scanner.stop_listening()

    def redirect_raw_recording(self, raw_data):
        data = self.sL.byte_stream_interpreter.interpret_rotation(raw_data)
        self.sL.sensor_data_processor.process_data(data)

    def update_selected(self):
        item = self.ui.tree_focus(self.tree)
        if item:
            data_item = self.sL.data.uuid_dict[item]
            if data_item[0] == DataLayers.gesture:
                self.selected_gesture = data_item[1].uuid
            elif data_item[0] == DataLayers.sample:
                self.selected_gesture = data_item[1].parent.uuid
                self.selected_sample = data_item[1].uuid
            elif data_item[0] == DataLayers.time_state:
                self.selected_gesture = data_item[1].parent.parent.uuid
                self.selected_sample = data_item[1].parent.uuid
                self.selected_time_state = data_item[1].uuid

    def reload_treeview(self):
        self.ui.tree_clear(self.tree)
        for gesture in self.sL.data.gestures:
            self.ui.add_to_tree(self.tree, gesture.name, "", gesture.uuid)
            for sample in gesture.samples:
                self.ui.add_to_tree(self.tree, sample.name, gesture.uuid, sample.uuid)
                for time_state in sample.time_states:
                    self.ui.add_to_tree(self.tree,
                                        "rot: " + str(time_state.rotation) + " / acc: " + str(time_state.acceleration),
                                        sample.uuid, time_state.uuid)
