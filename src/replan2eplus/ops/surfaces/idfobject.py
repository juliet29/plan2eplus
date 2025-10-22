from dataclasses import dataclass
from geomeppy import IDF
from typing import NamedTuple, TypedDict
from eppy.bunch_subclass import EpBunch
from replan2eplus.idfobjects.base import IDFObject
from replan2eplus.ezobjects.surface import Surface  # TODO rename!


@dataclass
class IDFSurface(IDFObject):
    @property
    def key(self):
        return "BUILDINGSURFACE:DETAILED"

    def create_ezobject(
        self, epbunch: EpBunch
    ):  # TODO instead of epbunch, specicif values..
        return Surface(epbunch)
