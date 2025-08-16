from dataclasses import dataclass
from eppy.bunch_subclass import EpBunch
import replan2eplus.epnames.keys as epkeys
from geomeppy import IDF as geomeppyIDF
from typing import TypedDict
from pathlib import Path
from eppy.modeleditor import IDDAlreadySetError
from typing import Literal, NamedTuple


# TODO move to Eppy constants
class GeomeppyBlock(TypedDict):
    name: str
    coordinates: list[tuple[float, float]]
    height: float


SubsurfaceKey = Literal["DOOR", "WINDOW", "DOOR:INTERZONE"]  # TODO copy in EPNames?


class SubsurfaceObject(NamedTuple):
    Name: str
    Building_Surface_Name: str
    # Outside_Boundary_Condition_Object: str
    Starting_X_Coordinate: float
    Starting_Z_Coordinate: float
    Length: float
    Height: float


@dataclass
class IDF:
    path_to_idd: Path
    path_to_idf: Path

    def __post_init__(self):
        try:
            geomeppyIDF.setiddname(self.path_to_idd)
        except IDDAlreadySetError:
            pass  # TODO log IDD already set, especially if the one they try to set is different..

        self.idf = geomeppyIDF(idfname=self.path_to_idf)

    # Geomepppy functions
    def print_idf(self):
        self.idf.printidf()  # TOOD make sure works?

    def add_geomeppy_block(self, block: GeomeppyBlock):
        # the order this has to follow should be based on the idf.. -> global
        self.idf.add_block(**block)

    def intersect_match(self):
        self.idf.intersect_match()

    def add_subsurface(self, key: SubsurfaceKey, subsurface_object: SubsurfaceObject):
        obj0 = self.idf.newidfobject(key.upper(), **subsurface_object._asdict())
        return obj0

    # My functions : )
    # TODO this is a property, unless adding filters later..
    def get_zones(self) -> list[EpBunch]:
        return [
            i for i in self.idf.idfobjects[epkeys.ZONE]
        ]  # TODO could put EzBunch on top here.. => maybe if things get out of hand..

    def get_surfaces(self) -> list[EpBunch]:
        return [i for i in self.idf.idfobjects[epkeys.SURFACE]]
