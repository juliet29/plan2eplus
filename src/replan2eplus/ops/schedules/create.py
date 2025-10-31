# TODO -> year -> schedule file object / interface -> schedule file object..
from pathlib import Path
from replan2eplus.ops.schedules.user_interface import ScheduleInput
from replan2eplus.ops.schedules.idfobject import IDFScheduleFile
from geomeppy import IDF
# from replan2eplus.ops.afn.utils import ScheduleInput


def create_schedule(idf: IDF, schedule_inputs: ScheduleInput, folder_path: Path):
    name, type_limits, year = schedule_inputs
    file_path = folder_path / name 
    idf_sched = IDFScheduleFile(name, type_limits, Path(file_path))
    year.write(folder_path)
    idf_sched.write(idf)

# def save_schedules(idf: IDF, folder_path: Path):
#     idf_schedules = IDFScheduleFile().read(idf)
#     for idf_sched in idf_schedules:
#         idf_sched.update_file_name(idf, folder_path)
