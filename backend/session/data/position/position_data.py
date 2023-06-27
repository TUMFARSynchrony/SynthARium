from dataclasses import dataclass

from session.data.base_data import BaseData
from session.data.position import PositionDict


@dataclass(slots=True)
class PositionData(BaseData):
    """Position data with update handling.

    Will forward any updates to the parent SessionData, making sure all changes are
    persistent.

    Attributes
    ----------
    x : int or float
        x-coordinate
    y : int or float
        y-coordinate
    z : int or float
        z-coordinate

    Methods
    -------
    asdict()
        Get PositionData as dictionary.

    Note
    ----
    Special methods, such as __init__, __str__, __repr__ and equality checks are
    generated automatically by dataclasses.dataclass.
    """

    x: int | float
    y: int | float
    z: int | float

    def asdict(self) -> PositionDict:
        """Get PositionData as dictionary.

        Returns
        -------
        custom_types.position.PositionDict
            PositionDict with the data in this PositionData.
        """
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }
