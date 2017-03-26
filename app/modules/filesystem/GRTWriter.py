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
        self.file.write("NumDimensions: 6" + "\n")
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
        self.file.write("UseExternalRanges: 0\n")
        self.file.write("LabelledTimeSeriesTrainingData:\n")

    def write_body(self):
        for i, gesture in enumerate(self.service_locator.data.gestures):
            for sample in gesture.samples:
                self.file.write("************TIME_SERIES************\n")
                self.file.write("ClassID: " + str(i + 1) + "\n")
                if self.write_raw:
                    self.file.write("SampleName: " + sample.name.replace("\n", "") + "\n")
                self.file.write("TimeSeriesLength: " + str(len(sample.time_states)) + "\n")
                self.file.write("TimeSeriesData:\n")
                for time_state in sample.time_states:
                    self.file.write(
                        str(time_state.rotation)[1:-1].replace(",", "") + " " + str(time_state.acceleration)[
                                                                                1:-1].replace(",", "") + "\n")

    def write_grtraw(self, file_path):
        """
        Writes the contents of the GRTWriter to the self.file specified

        Args:
            self.file_path (str): The full path to the self.file to which the contents should be written
        """

        self.file = open(file_path, "w")
        self.write_raw = True
        self.write_header()
        self.write_body()
        self.file.close()

    def write_grt(self, file_path):
        """
        Writes the contents of the GRTWriter to the self.file specified

        Args:
            self.file_path (str): The full path to the self.file to which the contents should be written
        """

        self.file = open(file_path, "w")
        self.write_raw = False
        self.write_header()
        self.write_body()
        self.file.close()
