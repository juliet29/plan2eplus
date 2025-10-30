from eppy.modeleditor import IDDAlreadySetError
from geomeppy import IDF


from pathlib import Path

from replan2eplus.ops.init.create import add_init_objects
from replan2eplus.paths import ep_paths


def open_idf(idf_path: Path | None = None):
    if idf_path:
        assert idf_path.exists(), f"Invalid idf path: {idf_path}"
        return IDF(idf_path)
    idf = IDF()
    idf.initnew(None)
    add_init_objects(
        idf
    )  # TODO ordinarily, need to do some checking to ensure that these objects dont already exist.., but they are not part of the ezobjects
    return idf


def initialize_idd():
    try:
        IDF.setiddname(ep_paths.idd_path)
    except IDDAlreadySetError:
        pass
