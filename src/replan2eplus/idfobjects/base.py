# TODO read some of these from config..

from typing import Any, Sequence
from geomeppy import IDF
from eppy.bunch_subclass import EpBunch
from dataclasses import dataclass


@dataclass
class IDFObject:
    @property
    def key(self) -> str: ...

    @property
    def values(self):
        return self.__dict__

    @classmethod
    def read(cls, idf: IDF, *args, **kwargs) -> Sequence:
        objects = idf.idfobjects[cls().key]
        return [cls(**get_object_description(i)) for i in objects]

    def write(self, idf: IDF):
        idf.newidfobject(self.key, **self.values)
        return idf

    # @classmethod
    # def read(cls, idf: IDF) -> list: ...
    def get_idf_objects(self, idf: IDF) -> list[EpBunch]:
        return idf.idfobjects[self.key]

    def create_ezobject(self, *args, **kwargs) -> Any: ...


def add_new_objects(idf: IDF, objects: list[IDFObject]):
    for object in objects:
        # TODO possibly log..
        # print(f"object key= {object.key}")
        # print(f"object kwargs= {object.values}")
        idf.newidfobject(object.key, **object.values)
    return idf


def get_object_description(object: EpBunch):
    d = {k: v for k, v in zip(object.fieldnames, object.fieldvalues)}
    d.pop("key")
    return d
