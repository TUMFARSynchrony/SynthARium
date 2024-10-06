import csv
import os
from typing import Any


class OpenFaceDataParser:
    def __init__(self, participant_id: str):
        # TODO: get session and participant id
        path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "sessions",
            "ae839e5e6f",
            "OpenFace",
        )
        filename = participant_id
        appendix = ".csv"

        if not os.path.exists(path):
            os.makedirs(path)

        filepath = os.path.join(path, filename + appendix)
        i = 1
        while os.path.exists(filepath):
            filepath = os.path.join(path, filename + f"_{i}" + appendix)
            i = i + 1

        self.save_file = open(filepath, "w")
        self.writer = csv.writer(self.save_file, delimiter=",")
        if participant_id == "aggregate":
            self.writer.writerow(
                ("Combination", "Time", "Runtime", "Non Aligned", "Aligned Data", "Aggregation Result"))
        else:
            self.writer.writerow(("TimeStap", "frame", "au06", "au12", "fps"))
        self.save_file.flush()

    def __del__(self):
        self.save_file.close()

    def write(self, timestapx, frame, au06, au12, fps):
        self.writer.writerow((timestapx, frame, au06, au12, fps))

    def write_ping(self, frame: int, ping: int):
        """Write ping data to the CSV."""
        self.writer.writerow((frame, ping))
        self.save_file.flush()

    def write_gf(self, c, time_value, runtime, non_aligned, data, result):
        """Write the relevant values to the CSV."""
        # Write the provided values as a row in the CSV
        self.writer.writerow((c, time_value, runtime, non_aligned, data, result))
        self.save_file.flush()
