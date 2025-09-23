from typing import Literal, NamedTuple


class SubsurfaceObject(NamedTuple):
    Name: str
    Building_Surface_Name: str
    Starting_X_Coordinate: float
    Starting_Z_Coordinate: float
    Length: float
    Height: float
    Outside_Boundary_Condition_Object: str = ""

    @property
    def values(self):
        vals = {
            k: v
            for k, v in self._asdict().items()
            if not (k == "Outside_Boundary_Condition_Object" and v == "")
        }
        return vals


SubsurfaceKey = Literal["DOOR", "WINDOW", "DOOR:INTERZONE"]
