from replan2eplus.ops.schedules.interfaces.constants import (
    START_DATE,
    DAY_START_TIME,
    DAY_END_TIME,
)


from datetime import date, datetime, time


def create_datetime(time_: time, date_: date = START_DATE):
    return datetime.combine(date_, time_)
