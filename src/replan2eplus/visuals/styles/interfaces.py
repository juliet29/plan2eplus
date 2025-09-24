from typing import Literal, TypedDict


FontSize = Literal[
    "xx-small", "x-small", "small", "medium", "large", "x-large", "xx-large"
]

NormedColor = tuple[float, float, float, float]

Color = Literal["navy", "deepskyblue", "gray", "snow", "saddlebrown", "white", "black"] | NormedColor
LineStyle = Literal[
    "-",
    "--",
    "-.",
    ":",
]

class BoundingBox(TypedDict):
    boxstyle: str
    ec: Color
    fc: Color
    alpha: int