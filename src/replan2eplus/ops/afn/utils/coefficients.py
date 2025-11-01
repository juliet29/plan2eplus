from geomeppy import IDF
from replan2eplus.geometry.directions import WallNormalLiteral, WallNormalNamesList
from replan2eplus.ops.afn.idfobject import (
    IDFAFNExternalNode,
    IDFAFNSurface,
    IDFAFNWindPressureCoefficientArray,
    IDFAFNWindPressureCoefficientValues,
)
from replan2eplus.ops.afn.user_interface import PressureCoefficientInput
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from rich import print
from expression.collections import Seq
from utils4plans.lists import sort_and_group_objects_dict


def make_wind_direction_object_name(ix: int = 0):
    return f"AFN_Wind_Directions_{ix}"


def make_wind_direction_entry_name(ix: int):
    return f"AFN_Wind_Directions_{ix}"


def make_coefficient_value_object_name(direction: WallNormalLiteral):
    return f"AFN_Pressure_Coefficient_Values_{direction}"


def make_coefficient_entry_object_name(ix: int):
    return f"Wind_Pressure_Coefficient_Value_{ix}"


def make_external_node_object_name(direction: WallNormalLiteral):
    return f"AFN_Pressure_Coefficient_Values_{direction}"


def create_pressure_objects(idf: IDF, input: PressureCoefficientInput):
    def make_external_nodes_and_coefficients(
        values: list[float],
        direction: WallNormalLiteral,
        wind_directions_object_name: str,
    ):
        value_dict = {
            make_coefficient_entry_object_name(ix): val for ix, val in enumerate(values)
        }
        coefficient_object_name = make_coefficient_value_object_name(direction)
        IDFAFNWindPressureCoefficientValues(
            coefficient_object_name, wind_directions_object_name, **value_dict
        ).write(idf)
        IDFAFNExternalNode(
            make_external_node_object_name(direction),
            Wind_Pressure_Coefficient_Curve_Name=coefficient_object_name,
        ).write(idf)

    wind_directions = {
        make_wind_direction_entry_name(ix): val
        for ix, val in enumerate(input.wind_directions)
    }

    wind_direction_object_name = make_wind_direction_object_name()
    IDFAFNWindPressureCoefficientArray(
        wind_direction_object_name, **wind_directions
    ).write(idf)

    for k, v in input.coefficient_values.items():
        make_external_nodes_and_coefficients(v, k, wind_direction_object_name)


def match_external_nodes(idf: IDF, afn_subsurfaces: list[Subsurface]):
    external_subsurfaces = (
        Seq(afn_subsurfaces).filter(lambda x: not x.neighbor_name).to_list()
    )

    print(external_subsurfaces)
    print(external_subsurfaces)

    groups: dict[WallNormalLiteral, list[Subsurface]] = sort_and_group_objects_dict(
        external_subsurfaces, lambda x: x.surface.direction
    )

    print(groups)
    for k, v in groups.items():
        external_node_name = make_external_node_object_name(k)
        for subsurface in v:
            IDFAFNSurface.update_afn_surface(
                idf,
                subsurface.subsurface_name,
                "External_Node_Name",
                external_node_name,
            )
