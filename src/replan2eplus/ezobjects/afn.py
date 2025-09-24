from dataclasses import dataclass
from replan2eplus.ezobjects.airboundary import Airboundary
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from utils4plans.sets import set_difference, set_intersection

@dataclass
class AirflowNetwork:
    zones: list[Zone]
    subsurfaces: list[Subsurface]
    airboundaries: list[Airboundary]

    # TODO post init to check that these actually are in the AFN!

    @property
    def surfacelike_objects(self):
        return self.subsurfaces + self.airboundaries

    def non_afn_airboundaries(self, airboundaries: list[Airboundary]):
        return [i for i in airboundaries if i not in self.airboundaries]

    def non_afn_subsurfaces(self, subsurfaces: list[Subsurface]):
        return [i for i in subsurfaces if i not in self.subsurfaces]

    def __rich_repr__(self):
        yield "zones", [i.zone_name for i in self.zones]
        yield "subsurfaces", [i.subsurface_name for i in self.subsurfaces]
        yield "airboundaries", [i.surface.surface_name for i in self.airboundaries]

    # def __str__(self) -> str:
    #     table = Table(AirflowNetwork)
    #     zone_names = [i.zone_name for i in self.zones]
    #     subsurface_names = [i.subs]
