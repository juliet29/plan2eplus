from replan2eplus.examples.cases.minimal import get_minimal_case_with_rooms
from replan2eplus.examples.subsurfaces import subsurface_inputs_dict


def make_afn_case():
    case = get_minimal_case_with_rooms()
    case.add_subsurfaces(subsurface_inputs_dict["three_details"])
    case.add_airflownetwork()
    return case
