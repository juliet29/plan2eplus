# Material Keys?
from typing import Literal, NamedTuple, get_args



#TODO this may not be the best home for this 
MaterialKey = Literal[
    "MATERIAL",
    "MATERIAL:AIRGAP",
    # "MATERIAL:INFRAREDTRANSPARENT",
    "MATERIAL:NOMASS",
    # "MATERIAL:ROOFVEGETATION",
    # "WINDOWMATERIAL:BLIND",
    "WINDOWMATERIAL:GLAZING",
    "WINDOWMATERIAL:GAS"
    # "WINDOWMATERIAL:GLAZING:REFRACTIONEXTINCTIONMETHOD",
    # "WINDOWMATERIAL:GAP",
    # "WINDOWMATERIAL:GAS",
    # "WINDOWMATERIAL:GASMIXTURE",
    # "WINDOWMATERIAL:GLAZINGGROUP:THERMOCHROMIC",
    # "WINDOWMATERIAL:SCREEN",
    # "WINDOWMATERIAL:SHADE",
    # "WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM",
]

material_keys = get_args(MaterialKey)


class MaterialObject(NamedTuple):
    Name: str
    Roughness: float
    Thickness: float
    Conductivity: float
    Density: float
    Specific_Heat: float
    Thermal_Absorptance: float
    Solar_Absorptance: float
    Visible_Absorptance: float

    # no:mass -> no density or thickness?

    # TODO depends on the type of material.. 


class ConstructionlObject(NamedTuple):
    Name: str
    OutsideLayer: str 
    
