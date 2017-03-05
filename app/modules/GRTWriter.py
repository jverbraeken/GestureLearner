def register(service_locator):
    GRTWriter.service_locator = service_locator
    service_locator.grt_writer = create


def create():
    return GRTWriter


class GRTWriter:
    classes = []
    current_class = 0
    service_locator = None

    def __init__(self, name, info_text):
        """
        Initialize a class that can write the data needed for the gesture recognition to a *.grt file

        Args:
            name (str): The name of the dataset
            info_text (str): A description of the dataset
        """
        self.name, self.info_text = name, info_text

    def add_class(self, name):
        """
        Add a new kind of gesture that the player can execute.
        Args:
            name (str): The name of the gesture
        """
        self.classes.append([])
        self.current_class += 1

    def add_sample(self, tuple_list):
        """
        Add a new series of rotation/acceleration data tuples that correspond to the execution of the last
        Args:
            tuple_list ():

        Returns:

        """
        self.classes[len(self.classes) - 1].append(tuple_list)

    def write_to_file(self, filepath):
        """
        Writes the contents of the GRTWriter to the file specified

        Args:
            filepath (str): The full path to the file to which the contents should be written

        """
        file = open(filepath, "w")
        file.write("GRT_LABELLED_TIME_SERIES_CLASSIFICATION_DATA_FILE_V1.0\n")
        file.write("DatasetName: " + self.name + "\n")
        file.write("InfoText: " + self.info_text + "\n")
        file.write("NumDimensions: 6" + "\n")
        file.close()
