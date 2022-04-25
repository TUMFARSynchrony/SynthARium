"""Provides the `ExperimentState` enum."""

from enum import Enum


class ExperimentState(Enum):
    """State a experiment is in.

    Initially, the state is `WAITING`. Connecting participants will be in the "waiting
    room" when joining in this state.

    When the experimenter starts the experiment, the state changes to `RUNNING`.
    Participants will then be in the running experiment room.

    When the experiment is stopped, the state switches to `ENDED`.
    """

    WAITING = 0
    RUNNING = 1
    ENDED = 2
