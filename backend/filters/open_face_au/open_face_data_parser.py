import csv
import os
import time

class OpenFaceDataParser:

    # TODO: get the action units based on what user needs
    HEADER = ["frame", "AU06", "AU12"]

    def __init__(self, session_id: str, participant_id: str):
        path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "sessions",
            session_id,
            "open_face_filter",
        )

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{participant_id}_{timestamp}.csv"

        if not os.path.exists(path):
            os.makedirs(path)

        filepath = os.path.join(path, filename)

        self.save_file = open(filepath, "w")
        self.writer = csv.writer(self.save_file, delimiter=",")
        self.writer.writerow(self.HEADER)

    def __del__(self):
        self.save_file.close()

    def write(self, frame: int, data: dict):
        row = [frame]
        for key in self.HEADER:
            if key in data["intensity"]:
                row.append(data["intensity"][key])
            else:
                row.append("-")

        self.writer.writerow(row)
