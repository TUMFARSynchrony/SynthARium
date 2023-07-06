import os
from multiprocessing import shared_memory
from NamedAtomicLock import NamedAtomicLock


starting_port: int = 5555
size: int = 2
lock_name: str = "open_face_lock"
lock_dir: str = os.path.dirname(os.path.abspath(__file__))
shm_name: str = "open_face_port"
shm: shared_memory.SharedMemory


def find_open_slot(current_slots: int, max_slots: int):
    for i in range(0, max_slots):
        first_free = current_slots & (1 << i)
        if not first_free:
            return i


# Remove old shared memory resources if there is any
try:
    shm = shared_memory.SharedMemory(name=shm_name, create=False, size=size)
    shm.close()
    shm.unlink()
except:
    pass


# Remove old lock if there is any
lock_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), lock_name)
if os.path.exists(lock_path):
    os.rmdir(lock_path)


class PortManager:
    _slot: int = 0
    _shared_port_slots: shared_memory.SharedMemory
    port: int

    global starting_port, size, lock_name, lock_dir, shm_name

    def __init__(self):
        self._lock = NamedAtomicLock(lock_name, lock_dir)
        self._lock.acquire()

        try:
            self._shared_port_slots = shared_memory.SharedMemory(
                name=shm_name, create=False, size=size
            )
        except:
            self._shared_port_slots = shared_memory.SharedMemory(
                name=shm_name, create=True, size=size
            )
            self._write_to_shared_memory(0)

        current_slots = self._read_from_shared_memory()
        self._slot = find_open_slot(current_slots, size * 8)

        next_slots = current_slots + (1 << self._slot)
        self._write_to_shared_memory(next_slots)

        self._lock.release()
        self.port = starting_port + self._slot

    def __del__(self):
        self._lock.acquire()
        current_slots = self._read_from_shared_memory()
        next_slots = current_slots - (1 << self._slot)
        self._write_to_shared_memory(next_slots)

        self._shared_port_slots.close()
        if next_slots == 0:
            self._shared_port_slots.unlink()

        self._lock.release()

    def _write_to_shared_memory(self, value: int) -> None:
        self._shared_port_slots.buf[:size] = bytearray(value.to_bytes(size, "big"))

    def _read_from_shared_memory(self) -> int:
        return int.from_bytes(bytes(self._shared_port_slots.buf[:size]), "big")
