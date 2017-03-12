# coding=utf-8
from app.modules.GRTWriter import GRTWriter


def register(service_locator):
    GRTWriter_Checked.service_locator = service_locator
    service_locator.grt_writer = GRTWriter_Checked("Placeholder Checked")


class GRTWriter_Checked(GRTWriter):
    def __init__(self, name):
        super(GRTWriter_Checked, self).__init__(name)
        self.name = name

    def add_class(self, name):
        super().add_class(name)

    def add_sample(self, class_name, tuple_list):
        if len(self.classes) == 0:
            raise RuntimeError("You must add at least one class to add sample to")
        if len(tuple_list) == 0:
            raise RuntimeError("The list of tuples must have a length of at least 1")
        for tuples in tuple_list:
            if len(tuples) != 6:
                raise RuntimeError(
                    "You should provide a rotation and acceleration (so 6 elements) in each tuple for each sample")

        super().add_sample(class_name, tuple_list)

    def write_to_file(self, file_path):
        super().write_to_file(file_path)
