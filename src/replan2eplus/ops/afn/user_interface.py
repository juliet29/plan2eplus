from typing import Literal, NamedTuple
from replan2eplus.ops.schedules.interfaces.year import Year
from replan2eplus.ops.schedules.user_interface import ScheduleInput
from replan2eplus.ops.schedules.interfaces.schedule_types import (
    UsefulScheduleTypeLimits,
)


class VentingInput(NamedTuple):
    selection: Literal["Doors", "Windows"]
    year: Year

    @property
    def schedule_name(self):
        return f"AFN_Venting_Schedule_for_{self.selection}"

    @property
    def schedule_input(self):
        return ScheduleInput(
            self.schedule_name, UsefulScheduleTypeLimits.Venting.Name, self.year
        )


class AFNInput(NamedTuple):
    venting_inputs: list[VentingInput]
