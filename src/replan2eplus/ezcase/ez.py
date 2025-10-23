from geomeppy import IDF
from dataclasses import dataclass
from eppy.modeleditor import IDDAlreadySetError
from pathlib import Path
from replan2eplus.ezcase.objects import read_existing_objects
from replan2eplus.ops.subsurfaces.create import create_subsurfaces
from replan2eplus.ops.subsurfaces.user_interfaces import SubsurfaceInputs
from replan2eplus.paths import ep_paths

from replan2eplus.ops.zones.user_interface import Room
from replan2eplus.ops.zones.create import create_zones

from typing import NamedTuple


def initialize_idd():
    try:
        IDF.setiddname(ep_paths.idd_path)
    except IDDAlreadySetError:
        pass


def open_idf(idf_path: Path | None = None):
    if idf_path:
        assert idf_path.exists(), f"Invalid idf path: {idf_path}"
        return IDF(idf_path)
    idf = IDF()
    idf.initnew(None)
    return idf


@dataclass
class EZ:
    idf_path: Path | None = None

    def __post_init__(self):
        initialize_idd()
        self.idf = open_idf(self.idf_path)
        self.objects = read_existing_objects(self.idf)

    def add_init_values(self):
        return self

    def add_zones(self, rooms: list[Room]):
        self.objects.zones, self.objects.surfaces = create_zones(self.idf, rooms)

        return self
    def add_subsurfaces(self, subsurface_inputs: SubsurfaceInputs):
        self.objects.subsurfaces = create_subsurfaces(subsurface_inputs, self.objects.surfaces, self.objects.zones, self.idf)
