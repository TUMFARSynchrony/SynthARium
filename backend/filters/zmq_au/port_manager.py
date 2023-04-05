from multiprocessing import shared_memory
from NamedAtomicLock import NamedAtomicLock


def find_open_slot(current_slots: int, max_slots: int):
    for i in range(0, max_slots):
        first_free = (current_slots & (1 << i))
        if not first_free:
            return i


class PortManager:
    _starting_port: int = 5555
    _slot: int = 0
    _shared_port_slots: shared_memory.SharedMemory
    _size: int = 2

    def __init__(self):
        self._lock = NamedAtomicLock("open_face_port")
        self._lock.acquire()

        try:
            self._shared_port: shared_memory.SharedMemory = shared_memory.SharedMemory(
                name="open_face_port", create=False, size=self._size)
        except:
            self._shared_port: shared_memory.SharedMemory = shared_memory.SharedMemory(
                name="open_face_port", create=True, size=self._size)
            self._shared_port.buf[:self._size] = bytearray((0).to_bytes(self._size, "big"))

        current_slots = int.from_bytes(bytes(self._shared_port.buf), "big")
        self._slot = find_open_slot(current_slots, self._size * 8)

        next_slots = current_slots + (1 << self._slot)
        self._shared_port.buf[:self._size] = bytearray(next_slots.to_bytes(self._size, "big"))

        self._lock.release()
        self.port = self._starting_port + self._slot

    def __del__(self):
        self._lock.acquire()
        current_slots = int.from_bytes(bytes(self._shared_port.buf), "big")
        next_slots = current_slots - (1 << self._slot)
        self._shared_port.buf[:self._size] = bytearray(next_slots.to_bytes(self._size, "big"))

        self._shared_port.close()
        if next_slots is 0:
            self._shared_port.unlink()

        self._lock.release()
