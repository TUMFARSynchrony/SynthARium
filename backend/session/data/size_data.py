from dataclasses import dataclass

from session.data.base_data import BaseData


@dataclass(slots=True)
class SizeData(BaseData):
    """Size data with update handling.

    Will forward any updates to the parent SessionData, making sure all changes are
    persistent.

    Attributes
    ----------
    width : int or float
    height : int or float

    Methods
    -------
    asdict()
        Get SizeData as dictionary.

    Note
    ----
    Special methods, such as __init__, __str__, __repr__ and equality checks are
    generated automatically by dataclasses.dataclass.
    """

    width: int | float
    height: int | float

    def asdict(self) -> SizeDict:
        """Get SizeData as dictionary.

        Returns
        -------
        custom_types.size.SizeDict
            SizeDict with the data in this SizeData.
        """
        return {
            "width": self.width,
            "height": self.height,
        }
