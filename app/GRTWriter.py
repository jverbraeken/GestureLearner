class GRTWriter:
    def __init__(self, name, info_text):
        """
        Initialize a class that can write the data needed for the gesture recognition to a *.grt file

        Args:
            name (str): The name of the dataset
            info_text (str): A description of the dataset
        """
        self.name = name
        self.info_text = info_text

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