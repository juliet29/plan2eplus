from dataclasses import dataclass
from utils4plans.lists import get_unique_one
from expression.collections import Seq

# from replan2eplus.ops.afn.interfaces import Neighborly
from replan2eplus.ops.airboundary.ezobject import Airboundary
from replan2eplus.ops.subsurfaces.ezobject import Subsurface
from replan2eplus.ops.zones.ezobject import Zone
from utils4plans.lists import chain_flatten_seq
from typing import Iterable
from typing import TypeVar

T = TypeVar("T")
K = TypeVar("K")

Neighborly = Subsurface | Airboundary


@dataclass
class AFNZone:
    name: str 
    surface_names: Iterable[str]


# # TODO come back to this later..
def get_matching_objects(
    param: str, curr_object_names: Seq[str], other_objects: Iterable[T]
) -> Seq[T]:
    return curr_object_names.map(
        lambda x: get_unique_one(
            other_objects, lambda obj: obj.__getattribute__(param) == x
        )
    )
    # return res


def get_avail_zones(zones: Iterable[Zone]):
    return (
        Seq(zones)
        .map(lambda x: AFNZone(x.zone_name, x.potential_afn_surface_names))
        .filter(lambda x: len(list(x.surface_names)) >= 2)
    ).to_list()


def get_avail_afn_zones(zones: Iterable[AFNZone]):
    return (Seq(zones).filter(lambda x: len(list(x.surface_names)) >= 2)).to_list()


def get_avail_surfaces(surfaces: Iterable[Neighborly], avail_zones: Iterable[AFNZone]):
    names = Seq(avail_zones).map(lambda x: x.surface_names).pipe(chain_flatten_seq)
    # avail_surfaces = names.map(
    #     lambda x: get_unique_one(surfaces, lambda obj: obj.name == x)
    # )

    return get_matching_objects("name", names, surfaces)
    #return avail_surfaces


def check_surfaces_for_nbs(surfaces: Seq[Neighborly]):
    names = surfaces.map(lambda x: x.name)

    def check_surface_nbs(surf: Neighborly):
        if surf.neighbor_name:
            if surf.neighbor_name not in names:
                return False
        return True

    return surfaces.filter(lambda x: check_surface_nbs(x)).to_list()


def update_zones(avail_zones: Iterable[AFNZone], avail_surfs: Iterable[Neighborly]):
    avail_surface_names = Seq(avail_surfs).map(lambda x: x.name)

    def update_zone_surfaces(zone: AFNZone):
        zone.surface_names = (
            Seq(zone.surface_names).filter(lambda x: x in avail_surface_names).to_list()
        )
        return zone

    return Seq(avail_zones).map(lambda x: update_zone_surfaces(x)).to_list()


def determine_afn_objects(zones: Iterable[Zone], surfaces: Iterable[Neighborly]):
    avail_zones = get_avail_zones(zones)
    avail_surfs = get_avail_surfaces(surfaces, avail_zones).pipe(check_surfaces_for_nbs)

    updated_zones = update_zones(avail_zones, avail_surfs)

    new_avail_zones = get_avail_afn_zones(updated_zones)
    new_avail_surfs = get_avail_surfaces(surfaces, new_avail_zones).to_list()

    afn_zones = Seq(new_avail_zones).map(lambda x: x.name).map(
        lambda x: get_unique_one(zones, lambda obj: obj.zone_name == x)
    ).to_list()

    # print(afn_zones)

    return list(afn_zones), list(new_avail_surfs)
    # return new_avail_zones, new_avail_surfs
