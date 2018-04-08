# coding=utf-8
import collections


def register(service_locator):
    GRTWriter.service_locator = service_locator
    service_locator.grt_writer = GRTWriter()


class GRTWriter:
    classes = collections.OrderedDict()
    service_locator = None
    file = None
    write_raw = False

    def __init__(self):
        """
        Initialize a class that can write the self.service_locator.data needed for the gesture recognition to a *.grt self.file
        """

    def write_header(self):
        def count_training_samples():
            count = 0
            for gesture in self.service_locator.data.gestures:
                count += len(gesture.samples)
            return count

        self.file.write("GRT_LABELLED_TIME_SERIES_CLASSIFICATION_DATA_FILE_V1.0\n")
        self.file.write("DatasetName: " + self.service_locator.data.name.replace("\n", "") + "\n")
        self.file.write("InfoText: " + self.service_locator.data.info.replace("\n", "") + "\n")
        self.file.write("TotalNumTrainingExamples: " + str(count_training_samples()) + "\n")
        self.file.write("NumberOfClasses: " + str(len(self.service_locator.data.gestures)) + "\n")
        self.file.write("ClassIDsAndCounters:\n")
        for i, val in enumerate(self.service_locator.data.gestures):
            self.file.write(str(i + 1) + "\t" + str(len(val.samples)) + "\n")
        if self.write_raw:
            self.file.write("ClassIDsAndNames:\n")
            for i, val in enumerate(self.service_locator.data.gestures):
                self.file.write(str(i + 1) + "\t" + val.name.replace("\n", "") + "\n")
            self.file.write("ClassIDsAndDescriptions:\n")
            for i, val in enumerate(self.service_locator.data.gestures):
                self.file.write(str(i + 1) + "\t" + val.description.replace("\n", "") + "\n")
        self.file.write("LabelledTimeSeriesTrainingData:\n")

    def write_body(self):
        for i, gesture in enumerate(self.service_locator.data.gestures):
            for sample in gesture.samples:
                self.file.write("************TIME_SERIES************\n")
                self.file.write("ClassID: " + str(i + 1) + "\n")
                if self.write_raw:
                    self.file.write("SampleName: " + sample.name.replace("\n", "") + "\n")
                self.file.write("TimeSeriesLength: " + str(len(sample.time_states)) + "\n")
                self.file.write("Duration: " + str(sample.time_states[-1].timestamp - sample.time_states[0].timestamp))
                self.file.write("TimeSeriesData:\n")
                if self.write_raw:
                    for time_state in sample.time_states:
                        self.file.write(
                            str((round(time_state.rotation[0]), round(time_state.rotation[1]), round(time_state.rotation[2])))[1:-1].replace(",", "")
                            + " "
                            + str((round(time_state.acceleration[0] * 100), round(time_state.acceleration[1] * 100), round(time_state.acceleration[2] * 100)))[1:-1].replace(",", "")
                            + " "
                            + str(time_state.timestamp)
                            + "\n")
                else:
                    for time_state in sample.time_states:
                        self.file.write(
                            str((round(time_state.rotation[0]), round(time_state.rotation[1]), round(time_state.rotation[2])))[1:-1].replace(",", "")
                            + " "
                            + str((round(time_state.acceleration[0] * 100), round(time_state.acceleration[1] * 100), round(time_state.acceleration[2] * 100)))[1:-1].replace(",", "")
                            + "\n")

    def write_grtraw(self, file_path):
        """
        Writes the contents of the GRTWriter to the file specified

        Args:
            self.file_path (str): The full path to the file to which the contents should be written
        """

        self.file = open(file_path, "w")
        self.write_raw = True
        self.write_header()
        self.write_body()
        self.file.close()

    def write_grt(self, file_path):
        """
        Writes the contents of the GRTWriter to the file specified

        Args:
            self.file_path (str): The full path to the file to which the contents should be written
        """

        self.file = open(file_path, "w")
        self.write_raw = False
        self.write_header()
        self.write_body()
        self.file.close()

    def write_uwf(self, file_path, captures):
        """
        Writes the contents of the uwf captures to the file specified

        Args:
            self.file_path (str): The full path to the file to which the contents should be written
        """
        gestures = self.service_locator.data.gestures

        self.file = open(file_path, "w")
        self.file.write(str(len(captures)) + "\n")
        for gesture in range(len(captures)):
            self.file.write(str(len(captures[gesture])) + "\n")
            self.file.write(gestures[gesture].name + "\n")
            for dimension in captures[gesture]:
                self.file.write(str(len(dimension)) + "\n")
                for capture in dimension:
                    self.file.write("CAPTURE\n")
                    self.file.write(str(capture.start_time) + "\n")
                    self.file.write(str(capture.end_time) + "\n")
                    self.file.write(str(capture.start_value) + "\n")
                    self.file.write(str(capture.end_value) + "\n")
                    self.file.write(str(capture.state) + "\n")
        self.file.close()
