from dataclasses import dataclass
from pathlib import Path
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.ezobjects.epbunch_utils import get_epbunch_key
from replan2eplus.zones.presentation import assign_zone_surfaces


def get_geom_objects(idf: IDF):
    zones = [Zone(i) for i in idf.get_zones()]
    surfaces = [Surface(i) for i in idf.get_surfaces()]
    updated_zones = assign_zone_surfaces(zones, surfaces)
    subsurfaces = [
        Subsurface.from_epbunch_and_key(i, updated_zones, surfaces)
        for i in idf.get_subsurfaces()
    ]

    return updated_zones, surfaces, subsurfaces


@dataclass
class ExistCase:
    path_to_idd: Path
    path_to_initial_idf: Path
    idf: IDF | None = None
    path_to_weather: Path = Path("") # TODO this should come from the idf!

    def __post_init__(self):
        self.initialize_idf()
        self.get_objects()

    def initialize_idf(self):
        self.idf = IDF(self.path_to_idd, self.path_to_initial_idf, self.path_to_weather)
        return self.idf

    def get_objects(self):
        assert self.idf
        self.zones, self.surfaces, self.subsurfaces = get_geom_objects(self.idf)

        return self.zones, self.surfaces, self.subsurfaces

    # TODO maybe this has a path, and then gets its on idf and sql results.. 