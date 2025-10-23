from typing import Literal
SurfaceType = Literal["floor", "wall", "ceiling", "roof"]
SunExposure = Literal["SunExposed", "NoSun"]
WindExposure = Literal["WindExposed", "NoWind"]

OutsideBoundaryCondition = Literal["Adiabatic", "Surface", "Outdoors", "Ground", "Founation", ""]
SurfaceCoords = list[tuple[float, float, float]]
