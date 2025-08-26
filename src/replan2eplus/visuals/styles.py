from typing import Literal, NamedTuple


class Alignment(NamedTuple):
    horizontalalignment: Literal["left", "center", "right"]
    verticalalignment: Literal["top", "center", "baseline", "bottom"]
    rotation: Literal["vertical"] | None = None
