# coding=utf-8
from tkinter import Frame, BOTH

from app.modules.logging import Loggers
from app.system import Constants

STRING_NEW_GESTURE = "New Gesture"
STRING_NEW_SAMPLE = "New Sample"
STRING_SAVE = "Save"
STRING_START_RECORDING = "Start Recording"
STRING_STOP_RECORDING = "Stop Recording"


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
        self.ui_bridge = self.sL.ui_bridge

        self.parent = parent
        self.parent.title(Constants.APPLICATION_NAME)
        self.pack(fill=BOTH, expand=1)
        self.ui_bridge.set_window_size(parent, Constants.WIDTH, Constants.HEIGHT)
        self.ui_bridge.create_tree(parent)

        self.ui_bridge.add_textbox(parent)
        self.ui_bridge.add_button(parent, STRING_NEW_GESTURE, self.create_new_gesture)
        self.ui_bridge.add_button(parent, STRING_NEW_SAMPLE, self.create_new_sample)
        self.ui_bridge.add_button(parent, STRING_SAVE, self.save)
        self.sL.ui_bridge.add_button(parent, STRING_START_RECORDING, self.start_recording)
        self.sL.ui_bridge.add_button(parent, STRING_STOP_RECORDING, self.stop_recording)
        self.logger = self.sL.logger_factory.get_logger(Loggers.ui)

    def create_new_gesture(self):
        """
        Create a new gesture
        """
        self.writer.add_class(self.ui_bridge.add_gesture())


    def create_new_sample(self):
        """
        Create a new gesture sample
        """
        self.writer.add_sample(self.ui_bridge.add_sample(), [(1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12)])
        self.logger.user_input("Button pressed: create_new_sample")
        self.writer.add_class("foo")

    def save(self):
        self.writer.write_to_file("C:/Users/Public/foo.grt")

    def start_recording(self):
        data = self.sL.data
        data.gestures[data.selected_gesture].add_sample()
        self.sL.udp_scanner.start_listening("0.0.0.0", 55056, self.redirect_raw_recording)

    def stop_recording(self):
        self.sL.udp_scanner.stop_listening()

    def redirect_raw_recording(self, raw_data):
        data = self.sL.byte_stream_interpreter.interpret_rotation(raw_data)
        self.sL.sensor_data_processor.process_data(data)
