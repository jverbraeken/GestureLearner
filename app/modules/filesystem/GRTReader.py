# coding=utf-8
import re

from app.modules.data import Data


def register(service_locator):
    GRTReader.service_locator = service_locator
    service_locator.grt_reader = GRTReader()


class GRTReader:
    service_locator = None

    def read_file(self, file_path):
        """
        Uses the data of the *.grt or *.grtraw to initialize a new data object that's used by the servicelocator
            automatically.

        Args:
            file_path (str): The full path where the *.grt or *.grtraw file resides
        """

        def read_file(file, data):
            def skip():
                pass

            class_ids_and_counters = []

            while True:
                line = file.readline()
                if not line:
                    break

                if line.startswith("GRT_LABELLED_TIME_SERIES_CLASSIFICATION_DATA_FILE_V1.0\n"):
                    skip()
                if line.startswith("DatasetName"):
                    data.name = line[line.index(':') + 2:-1]
                if line.startswith("InfoText"):
                    data.info = line[line.index(':') + 2:-1]
                if line.startswith("NumDimensions"):
                    skip()
                if line.startswith("TotalNumTrainingExamples"):
                    skip()
                if line.startswith("NumberOfClasses"):
                    num_classes_expected = int(line[line.index(':') + 2:-1])
                    for i in range(num_classes_expected):
                        data.add_gesture()
                if line.startswith("ClassIDsAndCounters"):
                    for i in range(num_classes_expected):
                        line = file.readline()
                        class_ids_and_counters.append(int(line.split("\t")[1]))
                if line.startswith("ClassIDsAndNames"):
                    for i in range(num_classes_expected):
                        line = file.readline()
                        data.gestures[i].name = line.split("\t")[1]
                if line.startswith("ClassIDsAndDescriptions"):
                    for i in range(num_classes_expected):
                        line = file.readline()
                        data.gestures[i].description = line.split("\t")[1]
                if line.startswith("UseExternalRanges"):
                    skip()
                if line.startswith("LabelledTimeSeriesTrainingData"):
                    for class_id in range(num_classes_expected):
                        for sample in range(class_ids_and_counters[class_id]):
                            file.readline() # **** TIME SERIES ****
                            file.readline()  # ClassID: ...
                            line = file.readline()
                            if line.startswith("SampleName"):
                                data.add_sample(line[line.index(':') + 2:-1])
                                line = file.readline()
                            else:
                                data.add_sample()
                            time_series_length = int(line[line.index(':') + 2:-1])
                            file.readline() # TimeSeriesData:
                            for rot in range(time_series_length):
                                line = file.readline()
                                nums = re.split("\W+", line)
                                data.add_time_state()
                                data.add_rotation((int(nums[0]), int(nums[1]), int(nums[2])))
                                data.add_acceleration((int(nums[3]), int(nums[4]), int(nums[5])))


        file = open(file_path, "r")
        Data.register(self.service_locator)
        data = self.service_locator.data
        read_file(file, data)
        file.close()