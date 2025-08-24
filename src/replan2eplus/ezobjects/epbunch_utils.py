# EPBunch helpers -> not worth it to have a class..
from eppy.bunch_subclass import EpBunch


def get_epbunch_key(epbunch: EpBunch):
    return epbunch.key



def create_dict_from_fields(epbunch: EpBunch):
    return {field: epbunch[field] for field in epbunch.objls if field != "key"}
