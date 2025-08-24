from dataclasses import dataclass
from pathlib import Path
from replan2eplus.airboundary.presentation import update_airboundary_constructions
from replan2eplus.ezobjects.airboundary import Airboundary
from replan2eplus.ezobjects.construction import Construction
from replan2eplus.ezobjects.material import Material
from replan2eplus.ezobjects.subsurface import Subsurface
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.constructions.presentation import (
    create_constructions_from_other_idf,
    check_materials_are_in_idf,
    find_and_add_materials,
    add_constructions,
    update_surfaces_with_construction_set,
)  # TODO really should pull up to init!
from replan2eplus.materials.presentation import (
    MaterialPair,
    add_materials,
    create_materials_from_other_idf,
)
from replan2eplus.subsurfaces.interfaces import SubsurfaceInputs
from replan2eplus.subsurfaces.logic import ZoneEdge
from replan2eplus.subsurfaces.presentation import create_subsurfaces
from replan2eplus.zones.interfaces import Room
from replan2eplus.zones.presentation import create_zones

# TODO: need to be aware that these might be called out of order, so do rigorous checks!  -> can use decorators for this maybe?


@dataclass
class EZCase:
    path_to_idd: Path
    path_to_initial_idf: Path

    # TODO: do these need to be initialized here?
    # path_to_weather: Path
    # path_to_analysis_period: AnalysisPeriod
    def __post_init__(self):
        # TODO -> read the case first? here, assuming starting from scratcj..
        
        self.airboundaries: list[Airboundary] = []
        self.subsurfaces: list[Subsurface] = []

        # -> may call add materials / constructions several times..
        self.materials: list[Material] = []
        self.constructions: list[Construction] = []
    

    def initialize_idf(self):
        self.idf = IDF(self.path_to_idd, self.path_to_initial_idf)
        return self.idf

    def add_zones(self, rooms: list[Room]):
        # TODO - check that idf exists!
        self.zones, self.surfaces = create_zones(self.idf, rooms)
        # when do constructuins, these surfaces will be updated..
        return self

    def add_airboundaries(self, edges: list[ZoneEdge]):
        # check that surfaces exist..
        self.airboundaries = update_airboundary_constructions(
            self.idf, edges, self.zones
        )
        return self
    

    def add_subsurfaces(self, inputs: SubsurfaceInputs):
        # TODO: check that zones exist
        self.subsurfaces = create_subsurfaces(
            inputs, self.zones, self.idf
        )  # TODO change so IDF comes first!
        return self


    def add_materials(self, material_pairs: list[MaterialPair]):
        add_materials(self.idf, material_pairs)
        return self

    def add_materials_from_other_idf(
        self, path_to_other_idf: Path, material_names: list[str] = []
    ):
        # NOTE: IDDs need to be the same -> geomeppy should throw an errow if they are not.. # TODO catch it!
        material_pairs = create_materials_from_other_idf(
            path_to_other_idf, self.path_to_idd, material_names=material_names
        )
        new_materials = add_materials(self.idf, material_pairs)
        self.materials.extend(new_materials)
        # TODO something to handle duplicates?

        return self
    
    # TODO: option to add constructions manually! 

    def add_constructions_from_other_idf(
        self,
        path_to_other_idf: Path,
        construction_names: list[str] = [],
        path_to_idfs_for_materials: list[Path] = [],
    ):
        construction_objects = create_constructions_from_other_idf(
            path_to_other_idf, self.path_to_idd, construction_names
        )

        if path_to_idfs_for_materials:
            new_materials = find_and_add_materials(
                self.idf,
                construction_objects,
                path_to_idfs_for_materials,
                self.path_to_idd,
            )
            self.materials.extend(new_materials)

        new_constructions = add_constructions(self.idf, construction_objects)
        self.constructions.extend(new_constructions)
        return self

    def add_airflownetwork(self):
        return self  # TODO: include airboundaries!

    def add_output_variables(self):
        return self  # use Munch!

    def save_and_run_case(self):
        return self  # compare to see if idf has changed or not -> interactive -> do you want to overwrite existing reults..


if __name__ == "__main__":
    pass
