from dataclasses import dataclass
from replan2eplus.idfobjects.base import IDFObject
from replan2eplus.ops.airboundary.interfaces import DEFAULT_AIRBOUNDARY_NAME


@dataclass
class IDFAirboundaryConstruction(IDFObject):
    Name: str = DEFAULT_AIRBOUNDARY_NAME
    # remaining fields are ignored when AFN is active
    Air_Exchange_Method: str = "SimpleMixing"  # or None..
    Simple_Mixing_Air_Changes_per_Hour: float = 0.5
    Simple_Mixing_Schedule_Name: str = ""  # otherwise reference a schedulr

    @property
    def key(self):
        return "CONSTRUCTION:AIRBOUNDARY"
