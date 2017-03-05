def register(service_locator):
    GRTWriter.service_locator = service_locator
    service_locator.grt_writer = GRTWriter


class GRTWriter:
    classes = {}
    service_locator = None
    name, info_text = "", ""

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
        file = open(file_path, "w")
        file.write("GRT_LABELLED_TIME_SERIES_CLASSIFICATION_DATA_FILE_V1.0\n")
        file.write("DatasetName: " + self.name + "\n")
        file.write("InfoText: " + self.info_text + "\n")
        file.write("NumDimensions: 6" + "\n")
        file.close()
