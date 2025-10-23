from typing import NamedTuple


class MaterialExamples(NamedTuple):
    typical = "M06 300mm concrete block"
    no_mass = "Terrazzo - 25mm"
    window_gas = "AIR 6MM"
    window_glazing = "CLEAR 12MM"
    materials_across_idfs = [
        typical,
        no_mass,
        window_gas,
        window_glazing,
    ]


class ConstructionExamples(NamedTuple):
    ashrae = "Light Exterior Wall"
    window = "Sgl Clr 3mm"
    constructions_across_idfs = [ashrae, window]
