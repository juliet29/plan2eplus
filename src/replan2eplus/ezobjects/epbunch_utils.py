# EPBunch helpers -> not worth it to have a class..
from dataclasses import fields
from eppy.bunch_subclass import EpBunch


def get_epbunch_key(epbunch: EpBunch):
    return epbunch.key


def create_dict_from_fields(epbunch: EpBunch):
    res = {field: epbunch[field] for field in epbunch.objls if field != "key"}
    return {k: v for k, v in res.items() if v}


def classFromArgs(className, argDict):
    # TODO this is a temp solution! -> removes data that might be there!
    fieldSet = {f.name for f in fields(className) if f.init}
    filteredArgDict = {k: v for k, v in argDict.items() if k in fieldSet}
    return className(**filteredArgDict)
