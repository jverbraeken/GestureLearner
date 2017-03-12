# coding=utf-8
import collections


def register(service_locator):
    GRTWriter.service_locator = service_locator
    service_locator.grt_writer = GRTWriter("Placeholder")


class GRTWriter:
    classes = collections.OrderedDict()
    service_locator = None

    def __init__(self, name):
        """
        Initialize a class that can write the data needed for the gesture recognition to a *.grt file

        Args:
            name (str): The name of the dataset
        """
        self.name = name

    def add_class(self, name):
        """
        Add a new kind of gesture that the player can execute.
        Args:
            name (str): The name of the gesture
        """
        self.classes[name] = []

    def add_sample(self, class_name, tuple_list):
        """
        Add a new series of rotation/acceleration data tuples that correspond to the execution of the gesture
        classified by class_name

        Args:
            class_name (str): The name of the class to which the sample belongs
            tuple_list (list): A list of tuples of which the first 3 elements correspond to the X, Y and Z rotation and
            the last 3 elements correspond to the X, Y and Z acceleration
        """
        self.classes[class_name].append(tuple_list)

    def write_to_file(self, file_path):
        """
        Writes the contents of the GRTWriter to the file specified

        Args:
            file_path (str): The full path to the file to which the contents should be written
        """

        def write_header():
            def get_total_num_training_examples():
                count = 0
                for tuple_list in self.classes:
                    count += len(self.classes[tuple_list])
                return count

            file.write("GRT_LABELLED_TIME_SERIES_CLASSIFICATION_DATA_FILE_V1.0\n")
            file.write("DatasetName: " + self.name + "\n")
            file.write("InfoText: " + " ".join(self.classes.keys()) + "\n")
            file.write("NumDimensions: 6" + "\n")
            file.write("TotalNumTrainingExamples: " + str(get_total_num_training_examples()) + "\n")
            file.write("NumberOfClasses: " + str(len(self.classes)) + "\n")
            file.write("ClassIDsAndCounters:\n")
            for i, val in enumerate(self.classes):
                file.write(str(i + 1) + "\t" + str(len(self.classes[val])) + "\n")
            file.write("UseExternalRanges: 0\n")
            file.write("LabelledTimeSeriesTrainingData:\n")

        def write_body():
            for i, gesture in enumerate(self.classes):
                for sample in self.classes[gesture]:
                    file.write("************TIME_SERIES************\n")
                    file.write("ClassID: " + str(i + 1) + "\n")
                    file.write("TimeSeriesLength: " + str(len(sample)) + "\n")
                    file.write("TimeSeriesData:\n")
                    for tuple in sample:
                        file.write(str(tuple)[1:-1].replace(",", "") + "\n")

        file = open(file_path, "w")
        write_header()
        write_body()
        file.close()