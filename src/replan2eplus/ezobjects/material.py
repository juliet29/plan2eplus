from replan2eplus.ezobjects.base import EZObject
from dataclasses import dataclass
import replan2eplus.epnames.keys as epkeys
from replan2eplus.idfobjects.materials import MaterialKey # TODO potential circular import 

@dataclass
class Material(EZObject):
    expected_key: MaterialKey
    pass

@dataclass
class Construction(EZObject):
    expected_key = epkeys.CONSTRUCTION

    @property
    def materials(self):
        pass # TODO read materials from the layers of the epbunch.. 