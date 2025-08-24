from pathlib import Path
from utils4plans.sets import set_difference
from replan2eplus.ezobjects.epbunch_utils import create_dict_from_fields
from replan2eplus.idfobjects.idf import IDF
from replan2eplus.constructions.interfaces import ConstructionsObject
import replan2eplus.epnames.keys as epkeys

from replan2eplus.errors import IDFMisunderstandingError


def create_constructions_from_other_idf(
    path_to_idf: Path, path_to_idd: Path, construction_names: list[str] = []
):
    def check_construction_names():
        differing_names = set_difference(
            construction_names, [i.Name for i in epbunches]
        )
        if differing_names:
            raise IDFMisunderstandingError(
                f"No materials with names in {differing_names} exist in this IDF!"
            )

    other_idf = IDF(path_to_idd, path_to_idf)
    epbunches = other_idf.get_constructions()
    check_construction_names()

    if construction_names:
        epbunches = [i for i in epbunches if i.Name in construction_names]

    constructions = [
        ConstructionsObject(**create_dict_from_fields(i)) for i in epbunches
    ]

    return constructions


# TODO: when adding constructions to idf, fail if the constituent materials are not in the new idf..
