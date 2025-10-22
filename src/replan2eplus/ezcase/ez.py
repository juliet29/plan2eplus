from geomeppy import IDF
from dataclasses import dataclass
from eppy.modeleditor import IDDAlreadySetError
from pathlib import Path
from replan2eplus.paths import ep_paths


def initialize_idd():
    try:
        IDF.setiddname(ep_paths.idd_path)
    except IDDAlreadySetError:
        pass


def open_idf(idf_path: Path | None = None):
    if idf_path:
        assert idf_path.exists(), f"Invalid idf path: {idf_path}"
        return IDF(idf_path)
    idf = IDF()
    idf.initnew(None)
    return idf


@dataclass
class EZ:
    idf_path: Path | None = None

    def __post_init__(self):
        initialize_idd()
        self.idf = open_idf(self.idf_path)

    def add_init_values(self):
        return self

    def add_zones(self):
        return self
