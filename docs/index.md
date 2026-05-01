---
icon: lucide/rocket
---

# plan2eplus

## plan2eplus makes it easy to translate floor plan geometry into building energy models

plan2eplus is a Python library designed for authoring building energy models, with the aim of helping designers better understand the energy consumption and thermal performance of proposed buildings during the early stages of design. plan2eplus is designed for [EnergyPlus](https://energyplus.net/), a popular software for creating building energy models.

plan2eplus provides support for:

- Translating validated geometric information into EnergyPlus models
- Studying the impact of natural ventilation on thermal performance using EnergyPlus's AirflowNetwork
- Quickly visualizing input geometries as 2D plans
- Studying the impact of different floor plans on thermal performance

## About

Typical methods for creating an energy model for a given floor plan can be slow and error-prone. In a typical workflow, one might obtain the dimensions of the geometries of the components of their floorplan, redraw the geometry based on these dimensions, and then have another program generate the energy model. plan2eplus relieves the need to redraw geometries, making it possible for users to go directly from dimensions of the plan to energy models. The package exposes a series of user friendly objects that can either be defined in Python or in JSON files, making it easy to bring geometric information from a variety of venues.

plan2eplus is designed for early-stage, climate-aware architecture. As such, support for EnergyPlus's AirflowNetwork, which enables users to understand the potential benefits of using natural ventilation, is a first-order consideration. plan2eplus also provides methods for visualizing floor plans and various quantities of interest, enabling designers to quickly understand how their chosen design affects thermal performance. As part of this goal, plan2eplus also provides functionality to quickly generate a series of different designs and study the impact of changes.

## Links

**Tutorials**

- [Getting Started](tutorials/getting_started.md)
- [Simple Project](tutorials/simple_project.md)

**Guides**

- [Constructions](guides/constructions.md)
