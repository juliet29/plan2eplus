# Creating a Simple Project

This tutorial walks you through creating a simple, two-bedroom project using `plan2eplus`. This tutorial assumes you have completed the steps for [installation and configuration](). We begin by adding the needed imports.

```python
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

```

## Creating the Plan

Creating a new case begins by initializing an `EZ` object. This will hold a Pythonic IDF object in memory, allowing us to add on step by step.

After initializing the case, we create a simple two-room plan. The height of each room is defined to be 3 meters, while each of the rooms are 10m x 10m. We use `Domain` and `Range` objects to simplify the process of describing the room's geometry since both rooms are rectangular.

After initializing the rooms, we add the rooms to the case as zones.

```python
case = EZ()


# Add rooms to the plan
height = 3  # m
domain_1 = Domain(horz_range=Range(0, 10), vert_range=Range(0, 10))
r1 = Room(0, "room1", domain_1, height)

domain_2 = Domain(horz_range=Range(10, 20), vert_range=Range(0, 10))
r2 = Room(1, "room2", domain_2, height)
case.add_zones([r1, r2])


```

## Adding windows and doors

To add windows and doors (subsurfaces) to the model, we first have to define their geometry. `plan2eplus` enables us to define where on the wall we want to place the subsurface using the `Location` object. This `Location` aligns the bottom middle of a theoretical door with the bottom middle of the wall it will be placed on. See [placing subsurfaces]('docs/guides') for more details. We also define the `Dimension`. Finally, we let the program know that this detail is for a door by creating a `Detail` object with the location, dimension, and `type_` of "door".

We repeat a similar process for windows. We then create a simple dictionary that maps the name of the detail to the `Detail` objects we have created.

```python

door_location = Location("bm", "SOUTH", "SOUTH")
door_dimension = Dimension(width=0.75, height=1)
door_detail = Detail(dimension=door_dimension, location=door_location, type_="Door")

window_location = Location("mm", "CENTROID", "CENTROID")
window_dimension = Dimension(width=0.5, height=0.5)
window_detail = Detail(
    dimension=window_dimension, location=window_location, type_="Window"
)

details = {"door": door_detail, "window": window_detail}
```

After creating the details that describe the geometry of the subsurface, we can add doors and windows to the case as edges. We must distinguish between edges in-between zones and edges between zones and the interior. To let the program know which edges correspond to which subsurface detail, we create `EdgeGroup`s that reference a key in our dictionary of `details`.

Finally, we can create a `SubsurfaceInputs` object that holds information about all the edges and the details of their geometry.

```python

interior_edges = EdgeGroup([Edge("room1", "room2")], "door", "Zone_Zone")
exterior_edges = EdgeGroup(
    [Edge("room1", "NORTH"), Edge("room2", "NORTH"), Edge("room1", "SOUTH")],
    "window",
    "Zone_Direction",
)

case.add_subsurfaces(
    SubsurfaceInputs(edge_groups=[interior_edges, exterior_edges], details=details)
)

```

## Adding constructions

We can add default construction materials by simply calling the `add_constructions()` method. To learn more about creating custom construction sets, see [construction sets]().

```python

case.add_constructions()
```

At this point, we can visualize the case with the following code, which will give us a 2D view of the plan.

```python
bp = make_base_plot(case)
bp.show()

```

(TODO: add image of base plot.)

We can see the edges we have added and the paths that flow would theoretically follow. However, the doors and windows are greyed out. This is because they are not yet part of the Airflow Network. Our model will not consider flow passing through them.

## Adding the airflow network

We can fix this by activating the Airflow Network in our case. Here, we rely on the default configuration, but you can explore further configuration options in [Airflow Network]().

```python
case.add_airflow_network()
```

Now, when we visualize the case, we see that the doors and windows are distinguished, indicating they are part of the AFN.

## Running the case

Finally, we can run the case and visualize results. Here we save results to a folder called `sample_project`, but it can be named anything you like.

```python
save_path = Path("sample_project")
case.save_and_run(save=True, run=True, output_path=save_path)

```

We can see the results by looking at a plot of the pressure and flow in each room.

```python

dp = make_pressure_plot(
    idf_path=save_path / "out.idf",
    sql_path=save_path / "results/eplusout.sql"),
)
dp.show()
```
