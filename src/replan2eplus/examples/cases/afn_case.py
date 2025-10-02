from replan2eplus.examples.cases.minimal import get_minimal_case_with_rooms
from replan2eplus.examples.subsurfaces import three_details_subsurface_inputs


def make_afn_case():
    case = get_minimal_case_with_rooms()
    case.add_subsurfaces(three_details_subsurface_inputs.inputs)
    case.add_airflownetwork()
    return case
