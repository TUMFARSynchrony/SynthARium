import os


class OpenFaceInstantiator:
    def __init__(self):
        self.openface_process = os.popen("../../build/bin/OwnExtractor")

    def __del__(self):
        self.openface_process.close()
