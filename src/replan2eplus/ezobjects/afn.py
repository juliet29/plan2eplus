from dataclasses import dataclass
from replan2eplus.ezobjects.airboundary import Airboundary
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.ezobjects.zone import Zone

@dataclass
class AirflowNetwork:
    zones: list[Zone]
    subsurfaces: list[Subsurface]
    airboundaries: list[Airboundary]
    
    @property
    def surfacelike_objects(self):
        return self.subsurfaces + self.airboundaries