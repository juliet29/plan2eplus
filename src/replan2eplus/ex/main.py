from replan2eplus.ex.rooms import Rooms
from replan2eplus.ezcase.ez import EZ
from replan2eplus.paths import ep_paths


class UserInterfaces:
    rooms = Rooms()


class Cases:
    ui = UserInterfaces()

    @property
    def base(self):
        return EZ()

    @property
    def example(self):
        name = "AirflowNetwork3zVent.idf"
        path = ep_paths.example_files / name
        return EZ(path)


    @property
    def two_room(self):
        case = self.base
        case.add_zones(self.ui.rooms.two_room_list)
        return case
