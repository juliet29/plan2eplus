from typing import get_args
from replan2eplus.ops.output.interfaces import (
    Site_Variables,
    Zone_Variables,
    Surface_Variables,
)


default_variables = list(
    get_args(Site_Variables) + get_args(Zone_Variables) + get_args(Surface_Variables)
)
