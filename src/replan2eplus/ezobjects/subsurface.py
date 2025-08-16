from replan2eplus.ezobjects.object2D import EZObject2D
from dataclasses import dataclass
import replan2eplus.epnames.keys as epkeys
from replan2eplus.geometry.domain import Literal
from eppy.bunch_subclass import EpBunch

subsurface_options = ["DOOR", "WINDOW", "DOOR:INTERZONE"]

@dataclass
class Subsurface(EZObject2D):
    _epbunch: EpBunch
    expected_key: str

    def __post_init__(self):
        assert self.expected_key in subsurface_options

    @property
    def name(self):
        return self._epbunch.Name

    # TODO properties to add: surface, partner obj, connecting zones, "driving zones" (for the purpose of the AFN )
