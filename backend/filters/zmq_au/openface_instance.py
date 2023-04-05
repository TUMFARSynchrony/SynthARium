import os
import subprocess

from filters.zmq_au.openface_data_parser import OpenFaceDataParser
from filters.zmq_au.port_manager import PortManager


class OpenFaceInstance:
    def __init__(self, port: int):
        self._port_manager = PortManager()
        self.port = self._port_manager.port
        try:
            self.openface_process = subprocess.Popen(["../../build/bin/OwnExtractor", f"{self.port}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            pass

    def __del__(self):
        try:
            self.openface_process.terminate()
        except:
            print("heyoooo")
            pass
