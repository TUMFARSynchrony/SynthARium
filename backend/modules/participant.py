"""TODO document"""

from __future__ import annotations

import modules.experiment as _experiment
import modules.user as _user


class Participant(_user.User):
    """TODO document"""
    experiment: _experiment.Experiment

    def __init__(self):
        """TODO document"""
        pass

    def handle_message(self, message):
        """TODO document"""
        pass

    def kick(self, reason: str):
        """TODO document"""
        pass
