import csv
import os


class OpenFaceDataParser:
    def __init__(self):
        # TODO: get session and participant id
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "sessions",
            "ae839e5e6f",
            "OpenFace"
        )
        filename = "9ba5fdccde"
        appendix = ".csv"

        if not os.path.exists(path):
            os.makedirs(path)

        filepath = path + filename + appendix
        i = 1
        while os.path.exists(filepath):
            filepath = path + filename + f"_{i}" + appendix
            i = i + 1

        self.save_file = open(filepath, "w")
        self.writer = csv.writer(self.save_file, delimiter=",")

    def __del__(self):
        self.save_file.close()

    def write(self, frame: int, openface_data):
        self.writer.writerow((f"frame {frame}", openface_data))
