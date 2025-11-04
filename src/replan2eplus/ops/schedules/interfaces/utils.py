from replan2eplus.ops.schedules.interfaces.constants import (
    YEAR_START_DATE,
    DAY_START_TIME,
    DAY_END_TIME,
)


from datetime import date, datetime, time


def create_datetime(time_: time, date_: date = YEAR_START_DATE):
    return datetime.combine(date_, time_)


def create_datetime_from_date(date_: date, time_: time = DAY_START_TIME):
    return datetime.combine(date_, time_)
