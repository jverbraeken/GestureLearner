def register(service_locator):
    GRTWriter_Checked.service_locator = service_locator
    service_locator.grt_writer = create


def create():
    return GRTWriter_Checked


class GRTWriter_Checked:
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

        Args:
            name ():

        Returns:

        """
        self.classes.append([])
        self.current_class += 1

    def add_sample(self, tuple_list):
        """

        Args:
            tuple_list ():

        Returns:

        """
        if len(self.classes) == 0:
            raise RuntimeError("You must add at least one class to add sample to")
        if len(tuple_list) == 0:
            raise RuntimeError("The list of tuples must have a length of at least 1")
        for tuples in tuple_list:
            if len(tuples) != 6:
                raise RuntimeError(
                    "You should provide a rotation and acceleration (so 6 elements) in each tuple for each sample")
        self.classes[len(self.classes) - 1].append(tuple_list)

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
