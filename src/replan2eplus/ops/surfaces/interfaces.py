from typing import Literal
SurfaceType = Literal["floor", "wall", "ceiling", "roof"]
SunExposure = Literal["SunExposed", "NoSun"]
WindExposure = Literal["WindExposed", "NoWind"]

OutsideBoundaryCondition = Literal["adiabatic", "surface", "outdoors", "ground", "founation", ""]
SurfaceCoords = list[tuple[float, float, float]]
