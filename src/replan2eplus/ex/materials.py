from typing import NamedTuple


class MaterialExamples(NamedTuple):
    material = "M06 300mm concrete block"
    material_no_mass = "Terrazzo - 25mm"
    window_gas_materials = "AIR 6MM"
    window_material_glazing = "CLEAR 12MM"
    materials_across_idfs = [
        material,
        material_no_mass,
        window_gas_materials,
        window_material_glazing,
    ]
