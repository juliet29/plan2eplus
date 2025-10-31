# TODO read some of these from config..

from tkinter import E
from typing import Any, Sequence
from geomeppy import IDF
from eppy.bunch_subclass import EpBunch
from dataclasses import dataclass
from utils4plans.lists import get_unique_one


class InvalidObjectError(Exception):
    def __init__(self, object_: object, name: str) -> None:
        self.object_ = object_
        self.name = name

    def message(self):
        return f"No object found for type {self.object_} and name {self.name}"


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

    # TODO delete -> think the read by name is replaces this ..
    @classmethod
    def read(cls, idf: IDF, *args, **kwargs):
        objects = idf.idfobjects[cls().key]

        return [cls(**get_object_description(i)) for i in objects]

    @classmethod
    def read_and_filter(cls, idf: IDF, *args, **kwargs):
        objects = idf.idfobjects[cls().key]

        def filter_d(d: dict):
            return {k: v for k, v in d.items() if k in cls().values.keys()}

        return [cls(**filter_d(get_object_description(i))) for i in objects]

    @classmethod
    def read_by_name(cls, idf: IDF, names: list[str] = []):
        objects = idf.idfobjects[cls().key]
        if names:
            return [
                cls(**get_object_description(i)) for i in objects if i.Name in names
            ]
        return [cls(**get_object_description(i)) for i in objects]

    @classmethod
    def read_one_by_name(cls, idf: IDF, name: str):
        res = cls.read(idf, [name])
        assert len(res) == 1, f"Expected to get only one item, insted got {res}"
        return res[0]

    def write(self, idf: IDF):
        idf.newidfobject(self.key, **self.values)
        return idf

    # @classmethod
    # def read(cls, idf: IDF) -> list: ...
    def get_idf_objects(self, idf: IDF) -> list[EpBunch]:
        return idf.idfobjects[self.key]

    # TODO turn these all into class methods..
    def get_one_idf_object(self, idf: IDF, name: str) -> EpBunch:
        check_has_name_attribute(self) # TODO: the way to extend this is to pass in a lambda function, but just have the Name parameter be the default.. can use ___eq___ dunder method.. 
        try:
            object = get_unique_one(self.get_idf_objects(idf), lambda x: x.Name == name)
        except AssertionError:
            raise InvalidObjectError(self, name)
        return object

    def update(self, idf: IDF, object_name: str, param: str, new_value: str):
        object = self.get_one_idf_object(idf, object_name)
        assert param in [k for k in self.values.keys()]
        object[param] = new_value

    def create_ezobject(self, *args, **kwargs) -> Any: ...

    def overwrite(self, idf: IDF):
        existing_idf_objects = idf.idfobjects[self.key]
        for o in existing_idf_objects:
            idf.removeidfobject(o)

        self.write(idf)


# TODO -> delete dont think this is being used anywher
def add_new_objects(idf: IDF, objects: list[IDFObject]):
    for object in objects:
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
