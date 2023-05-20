import subprocess


class OpenFace:
    def __init__(self, port: int):
        try:
            self._openface_process = subprocess.Popen(["../../build/bin/OwnExtractor", f"{port}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            pass

    def __del__(self):
        try:
            self._openface_process.terminate()
        except:
            pass

    def flush_result(self):
        # This is a bit ugly/hacky, but it stops the stdout from overflowing
        print(self._openface_process.stdout.readline())
        print(self._openface_process.stdout.readline())
        print(self._openface_process.stdout.readline())
        print(self._openface_process.stdout.readline())
