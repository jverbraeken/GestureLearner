# coding=utf-8
import operator

from app.modules.data import DataLayers


def register(service_locator):
    Data.sL = service_locator
    service_locator.data = Data(service_locator)


class TimeState:
    def __init__(self, uuid, parent, zRotation, vector, acceleration):
        self.uuid = uuid
        self.parent = parent
        self.zRotation = zRotation
        self.vector = vector
        self.acceleration = acceleration

class Sample:
    def __init__(self, name, uuid, parent, time_states=None):
        self.name = name
        self.uuid = uuid
        self.parent = parent
        if time_states is not None:
            self.time_states = time_states
        else:
            self.time_states = []
        self.selected_time_state = None

    def add_time_state(self, uuid, zRotation, vector, acceleration):
        time_state = TimeState(uuid, self, zRotation, vector, acceleration)
        self.time_states.append(time_state)
        self.selected_time_state = len(self.time_states) - 1
        return time_state


class Gesture:

    def __init__(self, name, uuid):
        self.selected_sample = None
        self.name = name
        self.description = ""
        self.samples = []
        self.uuid = uuid

    def add_sample(self, name, uuid):
        sample = Sample(name, uuid, self)
        self.samples.append(sample)
        self.selected_sample = len(self.samples) - 1
        return sample

    def add_time_state(self, uuid, zRotation, vector, acceleration):
        return self.samples[self.selected_sample].add_time_state(uuid, zRotation, vector, acceleration)


class Data:

    def __init__(self, service_locator):
        self.sL = service_locator
        self.gestures = []
        self.name = "Undefined"
        self.info = "Undefined"
        self.selected_gesture = None
        self.uuid_dict = {}

    def get_selected_gesture(self):
        return self.gestures[self.selected_gesture]

    def get_selected_sample(self):
        selected_gesture = self.gestures[self.selected_gesture]
        return selected_gesture.samples[selected_gesture.selected_sample]

    def get_selected_time_state(self):
        selected_gesture = self.gestures[self.selected_gesture]
        selected_sample = selected_gesture.samples[selected_gesture.selected_sample]
        return selected_sample.time_states[selected_sample.selected_time_state]

    def add_gesture(self, name, uuid):
        gesture = Gesture(name, uuid)
        self.gestures.append(gesture)
        self.selected_gesture = len(self.gestures) - 1
        self.uuid_dict[str(uuid)] = (DataLayers.gesture, gesture)
        return gesture

    def add_sample(self, name, uuid, gesture):
        sample = gesture.add_sample(name, uuid)
        self.uuid_dict[str(uuid)] = (DataLayers.sample, sample)
        return sample

    def add_time_state(self, uuid, sample, zRotation, vector, acceleration):
        time_state = sample.add_time_state(uuid, zRotation, vector, acceleration)
        self.uuid_dict[str(uuid)] = (DataLayers.time_state, time_state)
        return time_state

    def delete_sample(self, sample):
        self.uuid_dict[str(sample)][1].parent.samples.remove(self.uuid_dict[str(sample)][1])
        del self.uuid_dict[str(sample)]

    def delete_time_state(self, time_state):
        self.uuid_dict[str(time_state)][1].parent.time_states.remove(self.uuid_dict[str(time_state)][1])
        del self.uuid_dict[str(time_state)]

    def get_gesture_sorted(self):
        return sorted(self.gestures, key=operator.itemgetter("name"))
