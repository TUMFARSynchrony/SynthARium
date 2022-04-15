"""TODO document"""

from __future__ import annotations

import modules.experiment as _experiment
import modules.hub as _hub
import modules.user as _user


class Experimenter(_user.User):
    """TODO document"""
    experiment: _experiment.Experiment
    hub: _hub.Hub

    def handle_message(self, message):
        """TODO document"""
        pass
