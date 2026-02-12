from typing import NamedTuple

from plan2eplus.ops.schedules.interfaces.year import Year


class ScheduleInput(NamedTuple):
    name: str  # TODO: should this have ".csv" suffix? Is this failing?
    schedule_type_limits_name: str
    year: Year
