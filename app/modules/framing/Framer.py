# coding=utf-8
from app.modules.data.Data import TimeState
from app.modules.framing import States

TO_RISING = 3
FROM_RISING_TO_FALLING = -5
FROM_RISING_TO_STABLE = -3
FROM_STABLE_TO_RISING = 3
FROM_STABLE_TO_FALLING = -3
FROM_FALLING_TO_RISING = 5
FROM_FALLING_TO_STABLE = 3


def register(service_locator):
    Framer.service_locator = service_locator
    service_locator.framer = Framer()


class Capture:
    def __init__(self, start_time, start_value, state):
        self.start_time = start_time
        self.end_time = None
        self.start_value = start_value
        self.end_value = None
        self.state = state


class Framer:
    service_locator = None

    def __init__(self):
        self.gesture_start = []
        self.gesture_end = []
        self.num_gestures = []
        self.gestures = []

    def getCaptures(self):
        self.gestures = self.service_locator.data.gestures

        self.initializeGestures(self.gestures)

        captures = []
        for gesture in range(self.gestures):
            captures.append([])
            for dimension in range(3):
                captures[-1].append([])
                for time_state in range(len(self.gestures[gesture].samples[0].time_states) - 1):
                    old_time_state = self.getTimeState(gesture, time_state)
                    new_time_state = self.getTimeState(gesture, time_state + 1)
                    if len(captures[-1][-1]) == 0:
                        if new_time_state.rotation[dimension] - old_time_state.rotation[dimension] >= TO_RISING:
                            captures[-1][-1].append(
                                Capture(old_time_state.timestamp, old_time_state.rotation[dimension], States.rising))
                        else:
                            captures[-1][-1].append(
                                Capture(old_time_state.timestamp, old_time_state.rotation[dimension], States.falling))
                    else:
                        if captures[-1][-1][-1].state == States.rising:
                            if new_time_state.timestamp - old_time_state.timestamp < FROM_RISING_TO_FALLING:
                                captures[-1][-1][-1].end_time = old_time_state.timestamp
                                captures[-1][-1][-1].end_value = old_time_state.rotation[dimension]
                                captures[-1][-1][-1].append(
                                    Capture(new_time_state.timestamp, new_time_state.rotation[dimension], States.falling))
                            elif new_time_state.timestamp - old_time_state.timestamp < FROM_RISING_TO_STABLE:
                                captures[-1][-1][-1].end_time = old_time_state.timestamp
                                captures[-1][-1][-1].end_value = old_time_state.rotation[dimension]
                                captures[-1][-1][-1].append(
                                    Capture(new_time_state.timestamp, new_time_state.rotation[dimension], States.stable))
                        elif captures[-1][-1][-1].state == States.stable:
                            if new_time_state.timestamp - old_time_state.timestamp >= FROM_STABLE_TO_RISING:
                                captures[-1][-1][-1].end_time = old_time_state.timestamp
                                captures[-1][-1][-1].end_value = old_time_state.rotation[dimension]
                                captures[-1][-1][-1].append(
                                    Capture(new_time_state.timestamp, new_time_state.rotation[dimension], States.falling))
                            elif new_time_state.timestamp - old_time_state.timestamp < FROM_STABLE_TO_FALLING:
                                captures[-1][-1][-1].end_time = old_time_state.timestamp
                                captures[-1][-1][-1].end_value = old_time_state.rotation[dimension]
                                captures[-1][-1][-1].append(
                                    Capture(new_time_state.timestamp, new_time_state.rotation[dimension], States.stable))
                        elif captures[-1][-1][-1].state == States.falling:
                            if new_time_state.timestamp - old_time_state.timestamp >= FROM_FALLING_TO_RISING:
                                captures[-1][-1][-1].end_time = old_time_state.timestamp
                                captures[-1][-1][-1].end_value = old_time_state.rotation[dimension]
                                captures[-1][-1][-1].append(
                                    Capture(new_time_state.timestamp, new_time_state.rotation[dimension], States.rising))
                            elif new_time_state.timestamp - old_time_state.timestamp >= FROM_FALLING_TO_STABLE:
                                captures[-1][-1][-1].end_time = old_time_state.timestamp
                                captures[-1][-1][-1].end_value = old_time_state.rotation[dimension]
                                captures[-1][-1][-1].append(
                                    Capture(new_time_state.timestamp, new_time_state.rotation[dimension], States.stable))
                if captures[-1][-1][-1].state == States.stable:
                    del captures[-1][-1][-1]
                else:
                    last_time_state = self.getTimeState(gesture, len(self.gestures[gesture].samples[0].time_states) - 1)
                    captures[-1][-1].end_time = last_time_state.timestamp
                    captures[-1][-1].end_value = last_time_state.rotation[dimension]

    def initializeGestures(self, gestures):
        for gesture in gestures:
            self.gesture_start.append(gesture.samples[0].time_states[0].timestamp)
            self.gesture_end.append(gesture.samples[0].time_states[-1].timestamp)
            self.num_gestures.append(len(gesture.samples[0].time_states))

    def getTimeState(self, gesture, time_state):
        progression = time_state / self.num_gestures[gesture]
        time = self.gesture_start[gesture] + (self.gesture_end[gesture] - self.gesture_start[gesture]) * progression
        time_states = self.gestures[gesture].samples[0].time_states
        for tmp_time_state in range(len(time_states) - 1):
            current_time_state = time_states[tmp_time_state]
            next_time_state = time_states[tmp_time_state + 1]
            if current_time_state.timestamp == time:
                return TimeState(None, None,
                                 current_time_state.rotation,
                                 current_time_state.acceleration,
                                 time)
            elif next_time_state.timestamp > time:
                time_too_much = time - current_time_state.timestamp
                time_to_next_state = next_time_state.timestamp - current_time_state.timestamp
                div = time_too_much / time_to_next_state
                diff_rotation = next_time_state.rotation - current_time_state.rotation
                diff_acceleration = next_time_state.acceleration - current_time_state.acceleration
                return TimeState(None, None,
                                 current_time_state.rotation + diff_rotation * div,
                                 current_time_state.acceleration + diff_acceleration * div,
                                 time)
