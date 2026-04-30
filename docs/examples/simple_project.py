from plan2eplus.ezcase.ez import EZ
from pathlib import Path
from plan2eplus.ops.subsurfaces.interfaces import Dimension, Edge, Location
from plan2eplus.ops.subsurfaces.user_interfaces import (
    Detail,
    EdgeGroup,
    SubsurfaceInputs,
)
from plan2eplus.ops.zones.user_interface import Room
from plan2eplus.geometry.domain import Domain
from plan2eplus.geometry.range import Range
from plan2eplus.visuals.simple_plots import make_base_plot, make_pressure_plot

# Installation

## Configuration
# make sure the epconfig is here!


## Creating the plan

case = EZ()


# Add rooms to the plan
height = 3  # m
domain_1 = Domain(horz_range=Range(0, 1), vert_range=Range(0, 1))
r1 = Room(0, "room1", domain_1, height)

domain_2 = Domain(horz_range=Range(1, 2), vert_range=Range(0, 1))
r2 = Room(1, "room2", domain_2, height)
case.add_zones([r1, r2])


# Adding windows and doors
# door
door_location = Location("mm", "CENTROID", "CENTROID")
door_dimension = Dimension(width=0.75, height=1)
door_detail = Detail(dimension=door_dimension, location=door_location, type_="Door")

# window
window_location = Location("bm", "SOUTH", "SOUTH")
window_dimension = Dimension(width=0.5, height=0.5)
window_detail = Detail(
    dimension=window_dimension, location=window_location, type_="Window"
)

# details dictionary
details = {"door": door_detail, "window": window_detail}


# subsurfaces
interior_edges = EdgeGroup([Edge("room1", "room2")], "door", "Zone_Zone")
exterior_edges = EdgeGroup(
    [Edge("room1", "NORTH"), Edge("room2", "NORTH"), Edge("room1", "SOUTH")],
    "window",
    "Zone_Direction",
)

case.add_subsurfaces(
    SubsurfaceInputs(edge_groups=[interior_edges, exterior_edges], details=details)
)


# Constructions
case.add_constructions()  # Has reasonable defaults built in, details on creating are in a seprate file..

# before we add the afn, we will see that all the surfaces are not in the AFN
bp = make_base_plot(case)
bp.show()

# after add the afn, now we see colors on the base plot
case.add_airflow_network()

bp2 = make_base_plot(case)
bp2.show()


case.save_and_run(save=True, run=True, output_path=Path("sample_project"))
dp = make_pressure_plot(
    idf_path=Path("sample_project/out.idf"),
    sql_path=Path("sample_project/results/eplusout.sql"),
)
dp.show()
