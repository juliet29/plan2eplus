from dataclasses import dataclass
from pathlib import Path
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ezobjects.surface import Surface
from replan2eplus.ezobjects.zone import Zone
from replan2eplus.ezobjects.subsurface import Subsurface, Edge
from replan2eplus.ezobjects.epbunch_utils import get_epbunch_key
from replan2eplus.ops.subsurfaces.utils import get_unique_subsurfaces
from replan2eplus.ops.zones.create import assign_zone_surfaces
from replan2eplus.idfobjects.afn import AFNKeys
from replan2eplus.ezobjects.afn import AirflowNetwork
from replan2eplus.ezobjects.airboundary import Airboundary, get_unique_airboundaries

from rich import print as rprint


def get_surface_edge(surface: Surface, zones: list[Zone], surfaces: list[Surface]):
    zone = [i for i in zones if i.zone_name == surface.zone_name][0]
    if surface.boundary_condition == "outdoors":
        edge = Edge(zone.room_name, surface.direction.name)
    else:
        nb_surface = [i for i in surfaces if i.surface_name == surface.neighbor][0]
        nb_zone = [i for i in zones if i.zone_name == nb_surface.zone_name][0]
        edge = Edge(zone.room_name, nb_zone.room_name)

    return edge


def create_airboudnary(surface: Surface, zones: list[Zone], surfaces: list[Surface]):
    edge = get_surface_edge(surface, zones, surfaces)
    return Airboundary(surface, edge)


def get_geom_objects(idf: IDF):
    zones = [Zone(i) for i in idf.get_zones()]
    surfaces = [Surface(i) for i in idf.get_surfaces()]
    updated_zones = assign_zone_surfaces(zones, surfaces)
    subsurfaces = [
        Subsurface.from_epbunch_and_key(i, updated_zones, surfaces)
        for i in idf.get_subsurfaces()
    ]
    airboundaries = [
        create_airboudnary(i, updated_zones, surfaces)
        for i in surfaces
        if i.is_airboundary
    ]

    return updated_zones, surfaces, subsurfaces, airboundaries


# TODO reconstruct the AFN ..


def get_afn_objects(
    idf: IDF,
    zones: list[Zone],
    subsurfaces: list[Subsurface],
    airboundaries: list[Airboundary],
):
    afn_objects = idf.get_afn_objects()

    zone_objects = [i for i in afn_objects if get_epbunch_key(i) == AFNKeys.ZONE.value]
    afn_zones = [i for i in zones if i.zone_name in [j.Zone_Name for j in zone_objects]]
    assert len(zone_objects) == len(afn_zones)

    surface_objects = [
        i for i in afn_objects if get_epbunch_key(i) == AFNKeys.SURFACE.value
    ]
    surface_names = [j.Surface_Name for j in surface_objects]

    afn_airboundaries = [
        i for i in airboundaries if i.surface.surface_name in surface_names
    ]

    afn_subsurfaces = [i for i in subsurfaces if i.subsurface_name in surface_names]

    assert len(afn_subsurfaces) + len(afn_airboundaries) == len(surface_objects)

    afn = AirflowNetwork(afn_zones, afn_subsurfaces, afn_airboundaries)
    return afn


@dataclass
class ExistCase:
    path_to_idd: Path
    path_to_initial_idf: Path  # TODO this should allow passing in a directory!
    # idf: IDF | None = None
    path_to_weather: Path = Path("")  # TODO this should come from the idf!

    def __post_init__(self):
        self.idf = IDF(self.path_to_idd, self.path_to_initial_idf, self.path_to_weather)
        self.get_objects()
        self.get_afn()

    @property
    def folder_name(self): 
        return self.path_to_initial_idf.parts[-2]

    @property
    def folder_path(self):
        return self.path_to_initial_idf.parent

    def get_objects(self):
        assert self.idf
        self.zones, self.surfaces, self.subsurfaces, self.airboundaries = (
            get_geom_objects(self.idf)
        )

        return self.zones, self.surfaces, self.subsurfaces, self.airboundaries

    def get_afn(self):
        self.airflownetwork = get_afn_objects(
            self.idf, self.zones, self.subsurfaces, self.airboundaries
        )
    @property
    def unique_subsurfaces(self):
        return get_unique_subsurfaces(self.subsurfaces)
    
    @property
    def unique_airboundaries(self):
        return get_unique_airboundaries(self.airboundaries)

    # should define unique subsurfaces, zone names in upper case, etc..
    # sql results all come in upper case for some reason .. even though on the idf is written in normal case..

    # TODO maybe this has a path, and then gets its on idf and sql results..
