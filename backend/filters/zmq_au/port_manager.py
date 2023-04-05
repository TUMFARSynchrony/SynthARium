from multiprocessing import shared_memory
from NamedAtomicLock import NamedAtomicLock


def find_open_slot(current_slots: int):
    for i in range(0, 8):
        first_free = (current_slots & (1 << i))
        if not first_free:
            return i


class PortManager:
    _starting_port: int = 5555
    _slot: int = 0
    _shared_port_slots: shared_memory.SharedMemory

    def __init__(self):
        self._lock = NamedAtomicLock("open_face_port")
        self._lock.acquire()

        try:
            self._shared_port: shared_memory.SharedMemory = shared_memory.SharedMemory(
                name="open_face_port", create=False, size=1)
        except:
            self._shared_port: shared_memory.SharedMemory = shared_memory.SharedMemory(
                name="open_face_port", create=True, size=1)
            self._shared_port.buf[:1] = bytearray((0).to_bytes(1, "big"))

        current_slots = int.from_bytes(bytes(self._shared_port.buf), "big")
        self._slot = find_open_slot(current_slots)

        next_slots = current_slots + (1 << self._slot)
        self._shared_port.buf[:1] = bytearray(next_slots.to_bytes(1, "big"))

        self._lock.release()
        self.port = self._starting_port + self._slot

    def __del__(self):
        self._lock.acquire()
        current_slots = int.from_bytes(bytes(self._shared_port.buf), "big")
        next_slots = current_slots - (1 << self._slot)
        self._shared_port.buf[:1] = bytearray(next_slots.to_bytes(1, "big"))

        self._shared_port.close()
        if next_slots is 0:
            self._shared_port.unlink()

        self._lock.release()
