from dataclasses import dataclass
from pathlib import Path

from replan2eplus.ops.run_settings.user_interfaces import (
    AnalysisPeriod,
    write_run_period_and_location,
    default_analysis_period,
)
from replan2eplus.paths import ep_paths
from replan2eplus.ezcase.objects import read_existing_objects

from replan2eplus.ezcase.utils import initialize_idd, open_idf
from replan2eplus.ops.constructions.create import create_constructions
from replan2eplus.ops.constructions.user_interface import (
    ConstructionInput,
    default_construction_input,
)
from replan2eplus.ops.subsurfaces.create import create_subsurfaces
from replan2eplus.ops.subsurfaces.interfaces import (
    Edge,
)
from replan2eplus.ops.subsurfaces.user_interfaces import SubsurfaceInputs

from replan2eplus.ops.airboundary.create import update_airboundary_constructions
from replan2eplus.ops.afn.create import create_afn_objects
from replan2eplus.ops.zones.create import create_zones
from replan2eplus.ops.zones.user_interface import Room
from utils4plans.io import get_or_make_folder_path


@dataclass
class EZ:
    idf_path: Path | None = None
    output_path: Path | None = None
    epw_path: Path | None = None
    analysis_period: AnalysisPeriod | None = None

    def __post_init__(self):
        initialize_idd()
        self.idf = open_idf(self.idf_path)
        self.objects = read_existing_objects(self.idf)

    def add_zones(self, rooms: list[Room]):
        self.objects.zones, self.objects.surfaces = create_zones(self.idf, rooms)
        return self

    def add_subsurfaces(
        self, subsurface_inputs: SubsurfaceInputs, airboundary_edges: list[Edge] = []
    ):
        self.objects.airboundaries = update_airboundary_constructions(
            self.idf, airboundary_edges, self.objects.zones
        )
        # TODO the airboundaries should be part of the subsurface inputs.. -> detail or airboundary description ..

        self.objects.subsurfaces = create_subsurfaces(
            subsurface_inputs, self.objects.surfaces, self.objects.zones, self.idf
        )
        return self

    def add_airflow_network(self):
        self.objects.airflow_network = create_afn_objects(
            self.idf,
            self.objects.zones,
            self.objects.subsurfaces,
            self.objects.airboundaries,
        )
        return self

    def add_constructions(
        self,
        construction_inputs: ConstructionInput = default_construction_input,  # TODO decide if the name will be singular or plural, also should the defaults be this high up?
    ):
        # TODO have a default construction set
        cpaths, mpaths, cset = (
            construction_inputs  # TODO: add construction inputs to function definition
        )
        create_constructions(
            self.idf,
            cpaths,
            mpaths,
            cset,
            self.objects.surfaces,
            self.objects.subsurfaces,
        )
        return self

    def save_and_run(
        self,
        output_path: Path | None = None,
        epw_path: Path | None = None,
        analysis_period: AnalysisPeriod | None = default_analysis_period,
        run=False,
    ):
        if not self.output_path:
            assert output_path
            self.output_path = output_path
        if not self.epw_path:
            assert epw_path
            self.epw_path = epw_path
        if not self.analysis_period:
            assert analysis_period
            self.analysis_period = analysis_period

        self.output_path = get_or_make_folder_path(
            self.output_path.parent, self.output_path.name
        )

        idf_path = self.output_path / ep_paths.idf_name
        results_path = self.output_path / ep_paths.results_path

        write_run_period_and_location(self.idf, self.analysis_period, self.epw_path)
        print("hi")

        self.idf.save(idf_path)

        if run:
            if not self.idf_path:
                self.idf.idfabsname = idf_path
            self.idf.epw = self.epw_path
            self.idf.run(output_directory=results_path)
