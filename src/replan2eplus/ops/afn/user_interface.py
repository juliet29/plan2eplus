from typing import Literal, NamedTuple, TypedDict, cast
from replan2eplus.ops.schedules.interfaces.year import Year
from replan2eplus.ops.schedules.user_interface import ScheduleInput
from replan2eplus.ops.schedules.interfaces.schedule_types import (
    UsefulScheduleTypeLimits,
)
from replan2eplus.ops.afn.defaults.wind_directions import wind_directions
from replan2eplus.ops.afn.defaults.pressure_coefficients import (
    north,
    south,
    east,
    west,
)


class AFNVentingInput(NamedTuple):
    selection: Literal["Doors", "Windows"]
    year: Year

    @property
    def schedule_name(self):
        # TODO this is not very descriptive in the event there is more than one schdeule that applies to doors / windows.. 
        return f"AFN_Venting_Schedule_for_{self.selection}.csv"

    @property
    def schedule_input(self):
        return ScheduleInput(
            self.schedule_name, UsefulScheduleTypeLimits.Venting.Name, self.year
        )


class PressureCoefficientValues(TypedDict):
    NORTH: list[float]
    SOUTH: list[float]
    EAST: list[float]
    WEST: list[float]


# TODO is this better than a named tuple?
default_pressure_coefficients: PressureCoefficientValues = {
    "NORTH": north,
    "SOUTH": south,
    "EAST": east,
    "WEST": west,
}


class PressureCoefficientInput(NamedTuple):
    wind_directions: list[float] = wind_directions
    coefficient_values: PressureCoefficientValues = default_pressure_coefficients


class AFNInput(NamedTuple):
    venting: list[AFNVentingInput] = []
    pressure_coefficients: PressureCoefficientInput = (
        PressureCoefficientInput()
    )  # assume one for now, single story, later may change with height?
