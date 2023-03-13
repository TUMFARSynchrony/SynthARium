import os


class OpenFaceInstantiator:
    def __init__(self):
        self.openface_process = os.popen("../../build/bin/OwnExtractor")

    #def open(self):
    #    self.openface_process = os.popen("../../build/bin/OwnExtractor")

    #def close(self):
    #    self.openface_process.close()

    # TODO: this causes the participant to be kicked off sometimes?
    def __del__(self):
        self.openface_process.close()
