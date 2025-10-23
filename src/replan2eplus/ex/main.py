from replan2eplus.ex.materials import ConstructionExamples, MaterialExamples
from replan2eplus.ex.rooms import Rooms
from replan2eplus.ex.subsurfaces import SubsurfaceInputExamples
from replan2eplus.ezcase.ez import EZ
from replan2eplus.paths import ep_paths


class Interfaces:
    rooms = Rooms()
    subsurfaces = SubsurfaceInputExamples()
    materials = MaterialExamples()
    constructions = ConstructionExamples()


class ExampleCase:
    name = "AirflowNetwork3zVent.idf"
    path = ep_paths.example_files / name
    case = EZ(path)
    basic_material_names = [
        "A1 - 1 IN STUCCO",
        "C4 - 4 IN COMMON BRICK",
        "E1 - 3 / 4 IN PLASTER OR GYP BOARD",
        "C6 - 8 IN CLAY TILE",
        "C10 - 8 IN HW CONCRETE",
        "E2 - 1 / 2 IN SLAG OR STONE",
        "E3 - 3 / 8 IN FELT AND MEMBRANE",
        "B5 - 1 IN DENSE INSULATION",
        "C12 - 2 IN HW CONCRETE",
        "1.375in-Solid-Core",
    ]
    window_glazing_material_names = ["WIN-LAY-GLASS-LIGHT"]
    mixed_subset_materials = basic_material_names[0:4] + window_glazing_material_names
    constructions = [
        "DOOR-CON",
        "EXTWALL80",
        "PARTITION06",
        "FLOOR SLAB 8 IN",
        "ROOF34",
        "WIN-CON-LIGHT",
    ]


class Cases:
    ui = Interfaces()

    @property
    def base(self):
        return EZ()

    @property
    def example(self):
        return ExampleCase.case

    @property
    def two_room(self):
        case = self.base
        case.add_zones(self.ui.rooms.two_room_list)
        return case

    @property
    def subsurfaces_simple(self):
        case = self.two_room
        case.add_subsurfaces(Interfaces.subsurfaces.simple)
        return case
