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
    materials_for_const_across_idfs = [
        "F08 Metal surface",
        "I02 50mm insulation board",
        "F04 Wall air space resistance",
        "G01a 19mm gypsum board",
        "CLEAR 3MM",
    ]
