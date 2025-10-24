# TODO read some of these from config..

from tkinter import E
from typing import Any, Sequence
from geomeppy import IDF
from eppy.bunch_subclass import EpBunch
from dataclasses import dataclass
from utils4plans.lists import get_unique_one


def get_object_description(object: EpBunch):
    d = {k: v for k, v in zip(object.fieldnames, object.fieldvalues)}
    d.pop("key")
    return d


def filter_relevant_values(existing_values: dict, relevant_values: dict):
    return {k: v for k, v in existing_values.items() if k in relevant_values.keys()}


@dataclass
class IDFObject:
    @property
    def key(self) -> str: ...

    @property
    def values(self):
        return self.__dict__

    @classmethod
    def read(cls, idf: IDF, *args, **kwargs):
        objects = idf.idfobjects[cls().key]
        return [cls(**get_object_description(i)) for i in objects]

    @classmethod
    def read_by_name(cls, idf: IDF, names: list[str] = []):  # pyright: ignore[reportIncompatibleMethodOverride]
        objects = idf.idfobjects[cls().key]
        if names:
            return [
                cls(**get_object_description(i)) for i in objects if i.Name in names
            ]
        return [cls(**get_object_description(i)) for i in objects]

    def write(self, idf: IDF):
        idf.newidfobject(self.key, **self.values)
        return idf

    # @classmethod
    # def read(cls, idf: IDF) -> list: ...
    def get_idf_objects(self, idf: IDF) -> list[EpBunch]:
        return idf.idfobjects[self.key]

    def update(self, idf: IDF, object_name: str, param: str, new_value: str):
        check_has_name_attribute(self)
        try:
            object = get_unique_one(
                self.get_idf_objects(idf), lambda x: x.Name == object_name
            )
        except AssertionError:
            raise Exception(
                f"No object with {object_name} found!: IDFObjects are: {self.get_idf_objects(idf)}"
            )
        assert param in [k for k in self.values.keys()]
        object[param] = new_value
        # object.__setattr__(param, new_value)
        # TODO check type of this?

    def create_ezobject(self, *args, **kwargs) -> Any: ...


def add_new_objects(idf: IDF, objects: list[IDFObject]):
    for object in objects:
        # TODO possibly log..
        # print(f"object key= {object.key}")
        # print(f"object kwargs= {object.values}")
        idf.newidfobject(object.key, **object.values)
    return idf


def check_has_name_attribute(obj: IDFObject):
    try:
        obj.__getattribute__("Name")
    except AttributeError:
        f"No attribute Name for objects of type: {type(object)}"


def get_names_of_idf_objects(objects: Sequence[IDFObject]):
    lst: list[str] = []
    for o in objects:
        try:
            name: str = o.__getattribute__("Name")
            lst.append(name)
        except AttributeError:
            f"No attribute Name for objects of type(s): {set([type(i) for i in objects])}"
    return lst
