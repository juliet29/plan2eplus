import numpy as np


from typing import Literal, NamedTuple

AXIS = Literal["X", "Y", "Z"]


class Plane(NamedTuple):
    axis: AXIS
    location: float

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Plane):
            return (
                bool(np.isclose(self.location, other.location))
                and self.axis == other.axis
            )
        return False
