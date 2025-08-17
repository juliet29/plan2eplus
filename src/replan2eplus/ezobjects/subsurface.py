from replan2eplus.ezobjects.base import EZObject
from dataclasses import dataclass
import replan2eplus.epnames.keys as epkeys
from replan2eplus.geometry.domain import Domain, Literal
from eppy.bunch_subclass import EpBunch

from replan2eplus.geometry.range import Range
from replan2eplus.ezobjects.surface import Surface

subsurface_options = ["DOOR", "WINDOW", "DOOR:INTERZONE"]


@dataclass
class Subsurface(EZObject):
    _epbunch: EpBunch
    expected_key: str
    surface: Surface

    def __post_init__(self):
        assert self.expected_key in subsurface_options

    @property
    def subsurface_name(self):
        return self._epbunch.Name

    @property
    def domain(self):
        surf_domain = self.surface.domain
        surface_min_horz = surf_domain.horz_range.min
        surface_min_vert = surf_domain.vert_range.min

        horz_min = surface_min_horz + float(self._epbunch.Starting_X_Coordinate)
        width = float(self._epbunch.Length)

        vert_min = surface_min_vert + float(self._epbunch.Starting_Z_Coordinate)
        height = float(self._epbunch.Height)

        horz_range = Range(horz_min, horz_min + width)
        vert_range = Range(vert_min, vert_min + height)

        return Domain(horz_range, vert_range, surf_domain.plane)
        # need the surface its on..

    # TODO properties to add: surface, partner obj, connecting zones, "driving zones" (for the purpose of the AFN )
