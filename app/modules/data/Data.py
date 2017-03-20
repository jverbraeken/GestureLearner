# coding=utf-8
import operator
import uuid

from app.modules.data import DataLayers


def register(service_locator):
    Data.sL = service_locator
    service_locator.data = Data(service_locator)


class TimeState:
    rotation = None
    acceleration = None
    uuid = None
    parent = None

    def __init__(self, uuid, parent):
        self.uuid = uuid
        self.parent = parent

    def add_rotation(self, tuple):
        self.rotation = tuple

    def add_acceleration(self, tuple):
        self.acceleration = tuple

class Sample:
    name = ""
    time_states = []
    selected_time_state = None
    uuid = None
    parent = None

    def __init__(self, uuid, parent, time_states=None):
        self.uuid = uuid
        self.parent = parent
        if time_states is not None:
            self.time_states = time_states

    def add_time_state(self, uuid):
        time_state = TimeState(uuid, self)
        self.time_states.append(time_state)
        self.selected_time_state = len(self.time_states) - 1
        return time_state

    def add_rotation(self, tuple):
        self.time_states[self.selected_time_state].add_rotation(tuple)

    def add_acceleration(self, tuple):
        self.time_states[self.selected_time_state].add_acceleration(tuple)


class Gesture:
    selected_sample = None
    name = ""
    description = ""
    samples = []
    uuid = None

    def __init__(self, name, uuid):
        self.uuid = uuid
        self.name = name

    def add_sample(self, name, uuid):
        sample = Sample(uuid, self)
        self.samples.append(sample)
        self.selected_sample = len(self.samples) - 1
        self.samples[self.selected_sample].name = name
        return sample

    def add_rotation(self, tuple):
        self.samples[self.selected_sample].add_rotation(tuple)

    def add_acceleration(self, tuple):
        self.samples[self.selected_sample].add_acceleration(tuple)

    def add_time_state(self, uuid):
        return self.samples[self.selected_sample].add_time_state()


class Data:
    sL = None
    gestures = []
    name = ""
    info = ""
    selected_gesture = None

    uuid_dict = {}

    def __init__(self, service_locator):
        self.sL = service_locator
        self.sL.sensor_data_processor.add_listener(self.SampleCreator(self))

    class SampleCreator:
        outer_class = None

        def __init__(self, outer_class):
            self.outer_class = outer_class

        def get_selected_sample(self):
            gestures = self.outer_class.gestures
            selected_gesture = gestures[self.outer_class.selected_gesture]
            return selected_gesture.samples[selected_gesture.selected_sample]

        def new_time_state(self):
            self.get_selected_sample().add_time_state(uuid.uuid4())

        def rotation_received(self, rot_tuple):
            self.get_selected_sample().add_rotation(rot_tuple)

        def acceleration_received(self, rot_tuple):
            self.get_selected_sample().add_acceleration(rot_tuple)

    def add_gesture(self, name, uuid):
        gesture = Gesture(name, uuid)
        self.gestures.append(gesture)
        self.selected_gesture = len(self.gestures) - 1
        self.uuid_dict[uuid] = (DataLayers.gesture, gesture)
        return gesture

    def add_sample(self, name, uuid, gesture):
        sample = gesture.add_sample(name, uuid)
        self.uuid_dict[uuid] = (DataLayers.sample, sample)
        return sample

    def add_time_state(self, uuid, sample):
        time_state = sample.add_time_state(uuid)
        self.uuid_dict[uuid] = (DataLayers.time_state, time_state)
        return time_state

    def add_rotation(self, tuple):
        self.gestures[self.selected_gesture].add_rotation(tuple)

    def add_acceleration(self, tuple):
        self.gestures[self.selected_gesture].add_acceleration(tuple)

    def get_gesture_sorted(self):
        return sorted(self.gestures, key=operator.itemgetter("name"))
