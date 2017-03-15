# coding=utf-8
import operator


def register(service_locator):
    Data.sL = service_locator
    service_locator.data = Data(service_locator)


class TimeState:
    rotation = None
    acceleration = None

    def add_rotation(self, tuple):
        self.rotation = tuple

    def add_acceleration(self, tuple):
        self.acceleration = tuple

class Sample:
    name = ""
    time_states = []
    selected_time_state = None

    def __init__(self, time_states=None):
        if time_states is not None:
            self.time_states = time_states

    def add_time_state(self):
        self.time_states.append(TimeState())
        self.selected_time_state = len(self.time_states) - 1

    def add_rotation(self, tuple):
        self.time_states[self.selected_time_state].add_rotation(tuple)

    def add_acceleration(self, tuple):
        self.time_states[self.selected_time_state].add_acceleration(tuple)


class Gesture:
    selected_sample = None
    name = ""
    description = ""
    samples = []

    def __init__(self, name):
        self.name = name

    def add_sample(self, name=""):
        self.samples.append(Sample())
        self.selected_sample = len(self.samples) - 1
        self.samples[self.selected_sample].name = name

    def add_rotation(self, tuple):
        self.samples[self.selected_sample].add_rotation(tuple)

    def add_acceleration(self, tuple):
        self.samples[self.selected_sample].add_acceleration(tuple)

    def add_time_state(self):
        self.samples[self.selected_sample].add_time_state()


class Data:
    sL = None
    gestures = []
    selected_gesture = 0
    name = ""
    info = ""

    def __init__(self, service_locator):
        self.sL = service_locator
        self.sL.sensor_data_processor.add_listener(self.SampleCreator(self))

    class SampleCreator:
        outer_class = None

        def __init__(self, outer_class):
            self.outer_class = outer_class

        def rotation_received(self, rot_tuple):
            gestures = self.outer_class.gestures
            selected_gesture = gestures[self.outer_class.selected_gesture]
            selected_gesture_sample = selected_gesture.samples[selected_gesture.selected_sample]
            selected_gesture_sample.rotations.append(rot_tuple)

    def add_gesture(self, name=""):
        gesture = Gesture(name)
        self.gestures.append(gesture)
        self.selected_gesture = len(self.gestures) - 1

    def add_sample(self, name=""):
        self.gestures[self.selected_gesture].add_sample(name)

    def add_time_state(self):
        self.gestures[self.selected_gesture].add_time_state()

    def add_rotation(self, tuple):
        self.gestures[self.selected_gesture].add_rotation(tuple)

    def add_acceleration(self, tuple):
        self.gestures[self.selected_gesture].add_acceleration(tuple)

    def get_gesture_sorted(self):
        return sorted(self.gestures, key=operator.itemgetter("name"))
