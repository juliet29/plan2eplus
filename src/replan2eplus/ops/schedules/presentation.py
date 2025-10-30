# TODO -> year -> schedule file object / interface -> schedule file object..

from replan2eplus.idfobjects.idf import IDF
from replan2eplus.ops.afn.utils import ScheduleInput


def create_schedule(idf: IDF, vent_schedule: ScheduleInput):
    existing_schedules = idf.get_schedules()
    if existing_schedules:
        if vent_schedule.name not in existing_schedules:
            vent_schedule.write_schedule_to_path()
            idf.add_schedule(
                vent_schedule.schedule_idf_object
            )  # TODO really schould be case. add schedule??

    # TODO meant to return the Schedule EZObject, if such exists..
