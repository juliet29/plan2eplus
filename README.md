# plan2eplus

## plan2eplus makes it easy to translate floor plan geometry into building energy models

plan2eplus is a Python library designed for authoring building energy models, with the aim of helping designers better understand the energy consumption and thermal performance of proposed building during the early stages of design. plan2eplus is designed for [EnergyPlus](https://energyplus.net/), a popular software for creating building energy models.

plan2eplus provides support for:

- Translating validated geometric information into EnergyPlus models
- Studying the impact of natural ventilation on thermal performance using EnergyPlus's AirflowNetwork
- Quickly visualizing input geometries as 2D plans
- Studying the impact of different floor plans on thermal performance

## About

Typical methods for creating an energy model for a given floor plan can be slow and error-prone. In a typical workflow, one might obtain the dimensions of the geometries of the components of their floorplan, redraw the geometry based on these dimensions, and then have another program generate the energy model. plan2eplus relieves the need to redraw geometries, making it possible for users to go directly from dimensions of the plan to energy models. The package exposes a series of user friendly objects that can either be defined in Python or in JSON files, making it easy bring geometric information from a variety of venues.

plan2eplus is designed for early-stage, climate-aware architecture. As such, support for EnergyPlus's AirflowNetwork, which enables users to understand the potential benefits of using natural ventilation, is a first-order consideration. plan2eplus also provides methods for visualizing floor plans and various quantities of interest, enabling designers to quickly understand how their chosen design affects thermal performance. As part of this goal, plan2eplus also provides functionality to quickly generate a series of different designs and study the impact of changes.

## Install

plan2eplus **will soon** hosted on pypi. It **will** be easy to install using traditional methods for Python package installation.

```bash
# with uv
uv install plan2eplus

# with pip
pip install plan2eplus
```

plan2eplus provides an interface to EnergyPlus, making it easy to author EnergyPlus models. In order to _run_ energy models on your device, you will need a local installation on EnergyPlus. You can download EnergyPlus [here](https://energyplus.net/downloads). Note: currently, plan2eplus has only been tested using EnergyPlus 22.1.

## Usage

Below is a basic example of a workflow for creating a simple model with two adjacent rooms. For more examples, please refer to the (forthcoming) documentation.

```python

from replan2eplus.ezcase.ez import EZ

from replan2eplus.ops.zones.user_interface import Room
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.range import Range

# define geometry - all values are in meters
domain1 = Domain(horz_range=Range(0,1), vert_range=Range(0,1))
domain2 = Domain(horz_range=Range(1,2), vert_range=Range(0,1))
height = 3.00

# define rooms
room1 = Room(id=0, name="room1", domain1, height)
room2 = Room(id=1, name="room2", domain2, height)
rooms = [room1, room2]

# define the case
case = (
    EZ()
    .add_zones(rooms)
    .add_subsurfaces(SubsurfaceInputs(edge_groups, details), airboundary_edges)
    .add_constructions()
)

# run the case
case.save_and_run()

```

## Contributing

Please contact <jnwagwu@stanford.edu> if you are interested in helping to make plan2eplus better!
