from plan2eplus.ops.base import IDFObject
from plan2eplus.ops.init.idfobject import (
    Building,
    GlobalGeometryRules,
    SimulationControl,
    Timestep,
    Version,
)


from geomeppy import IDF


def add_init_objects(
    idf: IDF,
    base_objects: list[IDFObject] = [
        Version(),
        Timestep(),
        Building(),
        GlobalGeometryRules(),
        SimulationControl(),
    ],
):
    for obj in base_objects:
        obj.write(idf)
    return idf
