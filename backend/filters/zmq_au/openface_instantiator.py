import os
import subprocess


class OpenFaceInstantiator:
    def __init__(self, port: int):
        #self.openface_process = os.popen("../../build/bin/OwnExtractor")
        try:
            self.openface_process = subprocess.Popen(["../../cmake-build-release/bin/OwnExtractor", f"{port}"])
        except:
            pass
        #self.openface_process = subprocess.Popen(["../../build/bin/OwnExtractor"])


    #def open(self):
    #    self.openface_process = os.popen("../../build/bin/OwnExtractor")

    #def close(self):
    #    self.openface_process.close()

    # TODO: this causes the participant to be kicked off sometimes?
    def __del__(self):
        try:
            #self.openface_process.close()
            self.openface_process.terminate()
        except:
            print("heyoooo")
            pass
