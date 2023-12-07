import csv
import os
import time

class OpenFaceDataParser:

    # TODO: get the action units based on what user needs
    HEADER = ["frame"]

    def __init__(self, session_id: str, participant_id: str, action_units: list):
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

        self.filepath = os.path.join(path, filename)

        self.save_file = open(self.filepath, "w")
        self.writer = csv.writer(self.save_file, delimiter=",")
        self.action_units = action_units
        for au in action_units:
            self.HEADER.append(au)

        self.writer.writerow(self.HEADER)
    
    def reset(self):
        os.remove(self.filepath)

    def __del__(self):
        self.save_file.close()

    def write(self, frame: int, data: dict):
        row = [frame]
        for key in self.action_units:
            if key in data["intensity"]:
                row.append(data["intensity"][key])
            else:
                row.append("-")

        self.writer.writerow(row)
        self.save_file.flush()
