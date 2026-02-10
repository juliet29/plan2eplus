import pyprojroot
from utils4plans.paths import StaticPaths
from dataclasses import dataclass

from pathlib import Path
from typing import NamedTuple


from pydantic_settings import (
    BaseSettings,
)
from pydantic import BaseModel


class Names(BaseModel):
    idd: str = "Energy+.idd"
    example_files: str = "ExampleFiles"
    weather_files: str = "WeatherData"
    data_sets: str = "DataSets"


class Defaults(BaseModel):
    weather: str = "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
    minimal_case: str = "Minimal.idf"


class ConstructionNames(BaseModel):
    mat_and_const_idf: str = "ASHRAE_2005_HOF_Materials.idf"
    window_const_idf: str = "WindowConstructs.idf"
    window_glass_idf: str = "WindowGlassMaterials.idf"
    window_gas_idf: str = "WindowGasMaterials.idf"


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(toml_file="config.toml", validate_default=True)
    path_to_ep_install: Path = Path("/Applications/EnergyPlus-22-2-0")

    names: Names = Names()
    defaults: Defaults = Defaults()
    construction_names: ConstructionNames = ConstructionNames()

    # @classmethod
    # def settings_customise_sources(
    #     cls,
    #     settings_cls: type[BaseSettings],
    #     init_settings: PydanticBaseSettingsSource,
    #     env_settings: PydanticBaseSettingsSource,
    #     dotenv_settings: PydanticBaseSettingsSource,
    #     file_secret_settings: PydanticBaseSettingsSource,
    # ) -> tuple[PydanticBaseSettingsSource, ...]:
    #     return (TomlConfigSettingsSource(settings_cls),)


class InvalidPathError(Exception):
    def __init__(self, name, path):
        self.message = f"Invalid `{name}`: {path} does not exist"


class ConstructionPaths(NamedTuple):
    mat_and_const_idf: Path
    window_const_idf: Path
    window_glass_idf: Path
    window_gas_idf: Path

    @property
    def material_idfs(self):
        return [self.mat_and_const_idf, self.window_glass_idf, self.window_gas_idf]

    @property
    def constructiin_idfs(self):
        return [self.mat_and_const_idf, self.window_const_idf]


@dataclass
class EpPaths:
    path_to_ep_install: Path
    names: Names
    defaults: Defaults
    construction_names: ConstructionNames
    minimal_case: Path | None = None
    idf_name = "out.idf"
    results_path = "results"
    sql_name = "eplusout.sql"

    def __post_init__(self):
        if not self.path_to_ep_install.exists():
            raise InvalidPathError("path_to_ep_install", self.path_to_ep_install)

    def check_path_is_valid_and_return(self, name: str):
        path = self.path_to_ep_install / name
        if not path:
            raise InvalidPathError(name, path)
        return path

    @property
    def idd_path(self):
        return self.check_path_is_valid_and_return(self.names.idd)

    @property
    def example_files(self):
        return self.check_path_is_valid_and_return(self.names.example_files)

    @property
    def weather_files(self):
        return self.check_path_is_valid_and_return(self.names.weather_files)

    @property
    def data_sets(self):
        return self.check_path_is_valid_and_return(self.names.data_sets)

    # TODO these need to be validated also
    @property
    def default_weather(self):
        return self.weather_files / self.defaults.weather

    @property
    def default_minimal_case(self):  # TODO better to start from scratch no?
        if not self.minimal_case:
            return self.example_files / self.defaults.minimal_case
        else:
            return self.minimal_case

    @property
    def construction_paths(self):
        return ConstructionPaths(
            self.data_sets / self.construction_names.mat_and_const_idf,
            self.data_sets / self.construction_names.window_const_idf,
            self.data_sets / self.construction_names.window_glass_idf,
            self.data_sets / self.construction_names.window_gas_idf,
        )

    def reset_minimal_case(self, path: Path):
        self.minimal_case = path


def load_ep_paths():
    s = Settings()
    EP_PATHS = EpPaths(s.path_to_ep_install, s.names, s.defaults, s.construction_names)
    return EP_PATHS


BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
static_paths = StaticPaths("", base_path=BASE_PATH)
ep_paths = load_ep_paths()


class DynamicPaths:
    THROWAWAY_PATH = BASE_PATH / "throwaway"
    results_for_tests = static_paths.models / "results_for_tests"
    trials = static_paths.models / "trials"
    ORTHO_CASE_RESULTS = results_for_tests / "ortho"
    CAMPAIGN_TESTS = results_for_tests / "campaigns"
    subsurface_examples = results_for_tests / "subsurface_examples"
    afn_examples = results_for_tests / "afn_examples"
    airboundary_examples = results_for_tests / "airboundary_examples"
    test_scheds = static_paths.temp / "test_scheds"
    ts_open = test_scheds / "open"
    ts_dynamic = test_scheds / "dynamic"
    ts_closed = test_scheds / "closed"


SEED = 1234
