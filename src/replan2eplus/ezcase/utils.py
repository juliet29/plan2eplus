from eppy.modeleditor import IDDAlreadySetError
from geomeppy import IDF


from pathlib import Path

from replan2eplus.paths import ep_paths


def open_idf(idf_path: Path | None = None):
    if idf_path:
        assert idf_path.exists(), f"Invalid idf path: {idf_path}"
        return IDF(idf_path)
    idf = IDF()
    idf.initnew(None)
    return idf


def initialize_idd():
    try:
        IDF.setiddname(ep_paths.idd_path)
    except IDDAlreadySetError:
        pass
