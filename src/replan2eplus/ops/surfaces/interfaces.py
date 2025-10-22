from typing import Literal
SurfaceType = Literal["Floor", "Wall", "Ceiling", "Roof"]
SunExposure = Literal["SunExposed", "NoSun"]
WindExposure = Literal["WindExposed", "NoWind"]

OutsideBoundaryCondition = Literal["Adiabatic", "Surface", "Outdoors", "Ground", "Founation", ""]
SurfaceCoords = list[tuple[float, float, float]]
