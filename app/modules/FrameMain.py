# coding=utf-8
from tkinter import Frame, BOTH

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


    def __init__(self, parent, service_locator):
        Frame.__init__(self, parent)

        self.sL = service_locator
        self.writer = self.sL.grt_writer
        self.reader = self.sL.grt_reader

        self.parent = parent
        self.parent.title(Constants.APPLICATION_NAME)
        self.pack(fill=BOTH, expand=1)
        self.sL.ui_bridge.set_window_size(parent, Constants.WIDTH, Constants.HEIGHT)
        self.sL.ui_bridge.create_tree(parent)

        self.sL.ui_bridge.add_textbox(parent)
        self.sL.ui_bridge.add_button(parent, STRING_NEW_GESTURE, self.create_new_gesture)
        self.sL.ui_bridge.add_button(parent, STRING_NEW_SAMPLE, self.create_new_sample)
        self.sL.ui_bridge.add_button(parent, STRING_NEW_TIME_STATE, self.create_new_time_state)
        self.sL.ui_bridge.add_button(parent, STRING_OPEN, self.open)
        self.sL.ui_bridge.add_button(parent, STRING_SAVE, self.save)
        self.sL.ui_bridge.add_button(parent, STRING_EXPORT, self.export)
        self.sL.ui_bridge.add_button(parent, STRING_START_RECORDING, self.start_recording)
        self.sL.ui_bridge.add_button(parent, STRING_STOP_RECORDING, self.stop_recording)
        self.logger = self.sL.logger_factory.get_logger(Loggers.ui)

    def create_new_gesture(self):
        """
        Create a new gesture
        """
        self.sL.ui_bridge.add_gesture()

        self.logger.user_input("Button pressed: create_new_gesture")
        self.sL.data.add_gesture("foo")

    def create_new_sample(self):
        """
        Create a new gesture sample
        """
        self.sL.ui_bridge.add_sample()
        self.logger.user_input("Button pressed: create_new_sample")
        self.sL.data.add_sample("bar")

    def create_new_time_state(self):
        """
        Create a new gesture sample time state (rotation / acceleration)
        """
        self.logger.user_input("Button pressed: create_new_time_state")
        self.sL.data.add_time_state()
        self.sL.data.add_rotation((0, 1, 2))
        self.sL.data.add_acceleration((3, 4, 5))

    def save(self):
        path = self.sL.ui_bridge.show_save_dialog(
            parent=self.parent,
            title=STRING_SAVE_DIALOG,
            initial_directory=Constants.INITIAL_SAVE_DIRECTORY,
            file_types=[("Raw Gesture Recognition Toolkit files", ".grtraw")],
            default_extension=".grtraw")
        if path != "":
            self.writer.write_grt(path)

    def export(self):
        path = self.sL.ui_bridge.show_save_dialog(
            parent=self.parent,
            title=STRING_SAVE_DIALOG,
            initial_directory=Constants.INITIAL_SAVE_DIRECTORY,
            file_types=[("Gesture Recognition Toolkit files", ".grt")],
            default_extension=".grt")
        if path != "":
            self.writer.write_grtraw(path)

    def open(self):
        path = self.sL.ui_bridge.show_open_dialog(
            parent=self.parent,
            title=STRING_OPEN_DIALOG,
            initial_directory=Constants.INITIAL_SAVE_DIRECTORY,
            file_types=[("Raw Gesture Recognition Toolkit files", ".grtraw"),
                        ("Gesture Recognition Toolkit files", ".grt")],
            default_extension=".grtraw")
        if path != "":
            self.reader.read_file(path)

    def start_recording(self):
        data = self.sL.data
        data.gestures[data.selected_gesture].add_sample()
        self.sL.udp_scanner.start_listening("0.0.0.0", 55056, self.redirect_raw_recording)

    def stop_recording(self):
        self.sL.udp_scanner.stop_listening()

    def redirect_raw_recording(self, raw_data):
        data = self.sL.byte_stream_interpreter.interpret_rotation(raw_data)
        self.sL.sensor_data_processor.process_data(data)
