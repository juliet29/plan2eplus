from dataclasses import dataclass

from replan2eplus.ops.airboundary.ezobject import Airboundary
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.zones.ezobject import Zone


@dataclass
class AirflowNetwork:
    zones: list[Zone]
    afn_surfaces: list[Subsurface | Airboundary]

    def __rich_repr__(self):
        yield "zones", [i.zone_name for i in self.zones]
        yield "afn_surfaces", [i.name for i in self.afn_surfaces]

    @property
    def subsurfaces(
        self,
    ) -> list[Subsurface]:  # TODO consider changing these go filters..
        return [i for i in self.afn_surfaces if isinstance(i, Subsurface)]

    @property
    def airboundaries(self) -> list[Airboundary]:
        return [i for i in self.afn_surfaces if isinstance(i, Airboundary)]

    def get_non_afn_surfaces(self, surfaces: list[Subsurface | Airboundary]):
        res = filter(
            lambda x: x.name
            not in map(
                lambda y: y.name,
                self.afn_surfaces,
            ),
            surfaces,
        )
        return list(res)

    # TODO post init to check that these actually are in the AFN!

    # def select_afn_subsurfaces(
    #     self, select_fx: Callable[[list[Subsurface]], list[Subsurface]]
    # ):
    #     return select_fx(self.subsurfaces)
    #     subsurface_names = [i.subs]
