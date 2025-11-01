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
    return f"Wind_Direction_{ix + 1}"


def make_coefficient_value_object_name(direction: WallNormalLiteral):
    return f"AFN_Pressure_Coefficient_Values_{direction}"


def make_coefficient_entry_object_name(ix: int):
    return f"Wind_Pressure_Coefficient_Value_{ix + 1}"


def make_external_node_object_name(direction: WallNormalLiteral, room_name: str):
    return f"AFN_Pressure_Coefficient_Values_{direction}_{room_name}"


def create_pressure_data(
    idf: IDF,
    input: PressureCoefficientInput,
):
    def make_coefficients(
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

    wind_directions = {
        make_wind_direction_entry_name(ix): val
        for ix, val in enumerate(input.wind_directions)
    }

    wind_direction_object_name = make_wind_direction_object_name()
    IDFAFNWindPressureCoefficientArray(
        wind_direction_object_name, **wind_directions
    ).write(idf)

    for direction, values in input.coefficient_values.items():
        make_coefficients(
            values,  # type: ignore
            direction,  # type: ignore
            wind_direction_object_name,  # type: ignore
        )  # pyright: ignore[reportArgumentType]


def create_external_node(idf: IDF, direction: WallNormalLiteral, room_name: str):
    coefficient_object_name = make_coefficient_value_object_name(direction)
    obj = IDFAFNExternalNode(
        make_external_node_object_name(direction, room_name),
        Wind_Pressure_Coefficient_Curve_Name=coefficient_object_name,
    )
    obj.write(idf)
    return obj


def assign_external_nodes(idf: IDF, afn_subsurfaces: list[Subsurface]):
    external_subsurfaces = (
        Seq(afn_subsurfaces).filter(lambda x: not x.neighbor_name).to_list()
    )

    for surf in external_subsurfaces:
        direction = surf.surface.direction.name
        obj = create_external_node(idf, direction, surf.surface.room_name)
        IDFAFNSurface.update_afn_surface(
            idf,
            surf.subsurface_name,
            "External_Node_Name",
            obj.Name,
        )

    # groups: dict[WallNormalLiteral, list[Subsurface]] = sort_and_group_objects_dict(
    #     external_subsurfaces, lambda x: x.surface.direction.name
    # )

    # # print(groups)
    # for k, v in groups.items():
    #     for subsurface in v:
    #         IDFAFNSurface.update_afn_surface(
    #             idf,
    #             subsurface.subsurface_name,
    #             "External_Node_Name",
    #             external_node_name,
    #         )
    # return list(groups.keys())
