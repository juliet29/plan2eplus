from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.contact_points import calculate_corner_points
from replan2eplus.ops.subsurfaces.interfaces import Dimension
from replan2eplus.geometry.range import Range
from replan2eplus.idfobjects.subsurface import SubsurfaceObject
from replan2eplus.ops.subsurfaces.config import DOMAIN_SHRINK_FACTOR
from replan2eplus.ops.subsurfaces.interfaces import Details


def compare_and_maybe_change_dimensions(detail: Details, domain: Domain):
    def compare_and_maybe_change_dimension(
        dimension: float, range_: Range, shrink_factor=DOMAIN_SHRINK_FACTOR
    ):
        if dimension >= range_.size:
            return range_.size * shrink_factor
        return dimension

    dimension = detail.dimension
    width = compare_and_maybe_change_dimension(dimension.width, domain.horz_range)
    height = compare_and_maybe_change_dimension(dimension.height, domain.vert_range)
    return Details(Dimension(width, height), detail.location, detail.type_)


def compare_range(range_: Range, subsurf_range_: Range):
    if subsurf_range_.min < range_.min or subsurf_range_.max > range_.max:
        raise Exception(
            f"Arrangement is invalid! Domain range: {range_}. Subsurface range: {subsurf_range_}"
        )  # TODO add more contxt!


def compare_domain(domain: Domain, subsurf_domain: Domain):
    compare_range(domain.horz_range, subsurf_domain.horz_range)
    compare_range(domain.vert_range, subsurf_domain.vert_range)


def create_ss_name(surface_name: str, detail: Details):
    if surface_name:
        return f"{detail.type_}__{surface_name}"
    else:
        return ""


# TODO this goes to logic! TODO number files in logic _04_indiv_subsurf
def prepare_object(
    surface_name: str,
    subsurf_domain: Domain,
    main_surface_domain: Domain,
    detail: Details,
    nb_surface_name: str = "",
):
    # HERE CHECK SUBSURF DOMAINS..
    compare_domain(main_surface_domain, subsurf_domain)

    subsurf_coord = calculate_corner_points(subsurf_domain).SOUTH_WEST
    surf_coord = calculate_corner_points(main_surface_domain).SOUTH_WEST
    coords = (
        subsurf_coord.x - surf_coord.x,
        subsurf_coord.y - surf_coord.y,
    )  # need to subtract the surface corner..
    dims = detail.dimension.as_tuple
    print(f"coords for surface: {surface_name} are {coords}")

    return SubsurfaceObject(
        create_ss_name(surface_name, detail),
        surface_name,
        *coords,
        *dims,
        Outside_Boundary_Condition_Object=create_ss_name(nb_surface_name, detail),
    )
