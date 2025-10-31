from typing import Literal

Site_Variables = Literal[
    "Site Wind Speed",
    "Site Wind Direction",
    "Site Outdoor Air Drybulb Temperature",
]

Zone_Variables = Literal[
    "Zone Mean Air Temperature",
    "AFN Zone Ventilation Volume",
    "AFN Zone Mixing Volume",
    "AFN Node Total Pressure",
    "AFN Zone Mixing Sensible Heat Gain Rate",
    "AFN Zone Mixing Sensible Heat Loss Rate",
    "AFN Zone Ventilation Sensible Heat Gain Rate",
    "AFN Zone Ventilation Sensible Heat Loss Rate",
    "AFN Zone Ventilation Air Change Rate",
]

Surface_Variables = Literal[
    "AFN Linkage Node 1 to Node 2 Volume Flow Rate",
    "AFN Linkage Node 2 to Node 1 Volume Flow Rate",
]


OutputVariables = Site_Variables | Zone_Variables | Surface_Variables
