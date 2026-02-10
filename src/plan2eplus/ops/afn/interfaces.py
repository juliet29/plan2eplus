from geomeppy import IDF
from plan2eplus.ops.afn.idfobject import (
    IDFAFNSimpleOpening,
    IDFAFNSimulationControl,
    IDFAFNSurface,
    IDFAFNZone,
)
from dataclasses import dataclass


def create_name(input_name: str):
    return f"SimpleOpening__{input_name}"

@dataclass
class AFNWriter:
    zone_names: list[str]
    sub_and_surface_names: list[str]

    def write(self, idf: IDF):
        IDFAFNSimulationControl().write(idf)

        for zone_name in self.zone_names:
            IDFAFNZone(zone_name).write(idf)

        for name in self.sub_and_surface_names:
            opening_name = create_name(name)
            IDFAFNSimpleOpening(opening_name).write(idf)
            IDFAFNSurface(name, opening_name).write(idf)

