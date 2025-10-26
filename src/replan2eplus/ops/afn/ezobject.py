
from dataclasses import dataclass
from typing import Callable
from replan2eplus.ops.airboundary.ezobject import Airboundary
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.surfaces.ezobject import Surface
from replan2eplus.ops.zones.ezobject import Zone
from utils4plans.sets import set_difference, set_intersection


@dataclass
class AirflowNetwork:
    zones: list[Zone]
    subsurfaces: list[Subsurface]
    airboundaries: list[Airboundary]

    # TODO post init to check that these actually are in the AFN!

    def __rich_repr__(self):
        yield "zones", [i.zone_name for i in self.zones]
        yield "subsurfaces", [i.subsurface_name for i in self.subsurfaces]
        yield "airboundaries", [i.surface.surface_name for i in self.airboundaries]

    @property
    def surfacelike_objects(self):
        return self.subsurfaces + self.airboundaries

    def non_afn_airboundaries(self, airboundaries: list[Airboundary]):
        return [i for i in airboundaries if i not in self.airboundaries]

    def non_afn_subsurfaces(self, subsurfaces: list[Subsurface]):
        return [i for i in subsurfaces if i not in self.subsurfaces]

    def select_afn_subsurfaces(
        self, select_fx: Callable[[list[Subsurface]], list[Subsurface]]
    ):
        return select_fx(self.subsurfaces)

    # def __str__(self) -> str:
    #     table = Table(AirflowNetwork)
    #     zone_names = [i.zone_name for i in self.zones]
    #     subsurface_names = [i.subs]
