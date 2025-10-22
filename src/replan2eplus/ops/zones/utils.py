from replan2eplus.ezobjects.zone import Zone
from utils4plans.lists import chain_flatten


def get_surfaces_from_zones(zones: list[Zone]):
    return chain_flatten([i.surfaces for i in zones])
