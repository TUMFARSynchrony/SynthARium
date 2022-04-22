"""TODO document"""

from enum import Enum


class ExperimentState(Enum):
    """TODO document"""

    PLANNED = 0
    WAITING = 1
    RUNNING = 2
    OVER = 3
