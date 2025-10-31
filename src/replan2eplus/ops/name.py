import re
from typing import Literal, NamedTuple

SurfaceTypes = Literal["Wall", "Floor", "Roof"]


class IDFName(NamedTuple):
    plan_name: str
    n_direction: str
    n_position: str



    @property
    def direction_number(self):
        assert self.n_direction
        return int(self.n_direction)

    @property
    def position_number(self):
        if self.n_position:
            return int(self.n_position.split("_")[1])
        else:
            return "Z" # TODO map to letters.. 

    @property
    def full_number(self):
        if self.position_number:
            return f"{self.direction_number}_{self.position_number}"
        else:
            return str(self.direction_number)



def decompose_idf_name(name: str):
    def match(pattern: re.Pattern[str]):
        m = pattern.search(name)
        if m:
            return m.group()
        else:
            return ""


    plan_name = re.compile(r"`(.*)`")
    n_direction = re.compile(r"\d{4}")
    n_position = re.compile(r"_\d{1,2}\b")

    s = IDFName(
        match(plan_name).replace("`", ""),
        match(n_direction),
        match(n_position),
    )

    return s
