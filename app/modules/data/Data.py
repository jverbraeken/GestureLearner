# coding=utf-8
import operator


def register(service_locator):
    Data.sL = service_locator
    service_locator.data = Data(service_locator)


class Sample:
    name = ""
    rotations = []
    accelerations = []

    def __init__(self, rotations=None, accelerations=None):
        if rotations is not None:
            self.rotations = rotations
        if accelerations is not None:
            self.accelerations = accelerations


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

    def add_rotation(self, tuple):
        selected_sample = self.gestures[self.selected_gesture].selected_sample
        self.gestures[self.selected_gesture].samples[selected_sample].rotations.append(tuple)

    def add_acceleration(self, tuple):
        selected_sample = self.gestures[self.selected_gesture].selected_sample
        self.gestures[self.selected_gesture].samples[selected_sample].accelerations.append(tuple)

    def get_gesture_sorted(self):
        return sorted(self.gestures, key=operator.itemgetter("name"))
