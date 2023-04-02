import os
import subprocess

from filters.zmq_au.port_manager import PortManager


class OpenFaceInstance:
    def __init__(self, port: int):
        self._port_manager = PortManager()
        self.port = self._port_manager.port
        try:
            self.openface_process = subprocess.Popen(["../../cmake-build-release/bin/OwnExtractor", f"{self.port}"], stdout=subprocess.PIPE)
        except:
            pass

    def __del__(self):
        try:
            self.openface_process.terminate()
        except:
            print("heyoooo")
            pass
