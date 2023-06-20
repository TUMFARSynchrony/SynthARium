import os
from multiprocessing import shared_memory
from NamedAtomicLock import NamedAtomicLock


def find_open_slot(current_slots: int, max_slots: int):
    for i in range(0, max_slots):
        first_free = current_slots & (1 << i)
        if not first_free:
            return i


class PortManager:
    _starting_port: int = 5555
    _slot: int = 0
    _size: int = 2
    _shared_port_slots: shared_memory.SharedMemory
    port: int

    def __init__(self):
        self._lock = NamedAtomicLock("open_face_port", os.path.dirname(os.path.abspath(__file__)))
        self._lock.acquire()

        try:
            self._shared_port_slots: shared_memory.SharedMemory = shared_memory.SharedMemory(
                name="open_face_port", create=False, size=self._size
            )
        except:
            self._shared_port_slots: shared_memory.SharedMemory = shared_memory.SharedMemory(
                name="open_face_port", create=True, size=self._size
            )
            self._write_to_shared_memory(0)

        current_slots = self._read_from_shared_memory()
        self._slot = find_open_slot(current_slots, self._size * 8)

        next_slots = current_slots + (1 << self._slot)
        self._write_to_shared_memory(next_slots)

        self._lock.release()
        self.port = self._starting_port + self._slot

    def __del__(self):
        self._lock.acquire()
        current_slots = self._read_from_shared_memory()
        next_slots = current_slots - (1 << self._slot)
        self._write_to_shared_memory(next_slots)

        self._shared_port_slots.close()
        if next_slots == 0:
            self._shared_port_slots.unlink()

        self._lock.release()

    def _write_to_shared_memory(self, value: int):
        self._shared_port_slots.buf[: self._size] = bytearray(
            value.to_bytes(self._size, "big")
        )

    def _read_from_shared_memory(self) -> int:
        return int.from_bytes(bytes(self._shared_port_slots.buf[: self._size]), "big")
