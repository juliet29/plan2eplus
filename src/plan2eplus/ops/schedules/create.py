# TODO -> year -> schedule file object / interface -> schedule file object..
from pathlib import Path
from plan2eplus.ops.schedules.user_interface import ScheduleInput
from plan2eplus.ops.schedules.idfobject import IDFScheduleFile
from geomeppy import IDF
# from plan2eplus.ops.afn.utils import ScheduleInput


def create_schedules(idf: IDF, schedule_inputs: list[ScheduleInput], folder_path: Path):
    def create(schedule: ScheduleInput):
        name, type_limits, year = schedule
        file_path = folder_path / name
        idf_sched = IDFScheduleFile(name, type_limits, Path(file_path))
        year.write_to_file(file_path)
        idf_sched.write(idf)

    for sched in schedule_inputs:
        create(sched)
