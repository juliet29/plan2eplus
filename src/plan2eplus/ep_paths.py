from dataclasses import dataclass, field
from omegaconf import MISSING, OmegaConf
from pathlib import Path

from plan2eplus.paths import DynamicPaths
from plan2eplus.errors import InvalidPathError
import os


@dataclass
class FileStructure:
    idd: str = "Energy+.idd"
    example_files: str = "ExampleFiles"
    weather_files: str = "WeatherData"
    data_sets: str = "DataSets"


@dataclass
class ConstructionNames:
    mat_and_const_idf: str = "ASHRAE_2005_HOF_Materials.idf"
    window_const_idf: str = "WindowConstructs.idf"
    window_glass_idf: str = "WindowGlassMaterials.idf"
    window_gas_idf: str = "WindowGasMaterials.idf"

    @property
    def material_idfs(self):
        return [self.mat_and_const_idf, self.window_glass_idf, self.window_gas_idf]

    @property
    def construction_idfs(self):
        return [self.mat_and_const_idf, self.window_const_idf]


@dataclass
class EpConfig:
    path_to_ep_install: Path = MISSING
    ep_dir: FileStructure = field(default_factory=FileStructure)
    default_weather: str = "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
    default_constructions: ConstructionNames = field(default_factory=ConstructionNames)


@dataclass
class EpPaths:

    def __post_init__(self):
        # TODO: the path should be very unique path... like epconfig, so it doesnt clash with other configs...
        # TODO: check that project will know to look for these configs in the root ... -> instructions for this should be very clear in the readme..
        user_config_path = DynamicPaths.config / "user.yaml"
        user_config = (
            OmegaConf.load(user_config_path) if user_config_path.exists() else {}
        )
        # this will depend on the environment..
        current_env = os.environ.get("APP_ENV")
        print(f"Current environment: {current_env}")

        if not current_env:
            current_env = "dev"
        local_config = OmegaConf.load(DynamicPaths.config / f"{current_env}.yaml")

        schema = OmegaConf.structured(EpConfig)

        config = OmegaConf.merge(
            schema, local_config, user_config
        )  # this step should be checking the schemas..

        self.config: EpConfig = OmegaConf.to_object(
            config
        )  # pyright: ignore[reportAttributeAccessIssue]

    def get_path(self, name: str | Path):
        path = self.config.path_to_ep_install / name
        if not path:  # TODO: change to path.exists()
            raise InvalidPathError(name, path)
        return path

    @property
    def idd_path(self):
        return self.get_path(self.config.ep_dir.idd)

    @property
    def default_weather(self):
        return self.get_path(
            Path(self.config.ep_dir.weather_files) / self.config.default_weather
        )

    @property
    def example_files(self):
        return self.get_path(self.config.ep_dir.example_files)

    @property
    def material_idfs(self):
        return [
            self.get_path(Path(self.config.ep_dir.data_sets) / i)
            for i in self.config.default_constructions.material_idfs
        ]

    @property
    def construction_idfs(self):
        return [
            self.get_path(Path(self.config.ep_dir.data_sets) / i)
            for i in self.config.default_constructions.construction_idfs
        ]


ep_paths = EpPaths()
