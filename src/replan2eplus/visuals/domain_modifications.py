from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.range import compute_multirange, expand_range

# again, as bounding box!


def compute_multidomain(domains: list[Domain]):
    horz_range = compute_multirange([i.horz_range for i in domains])
    vert_range = compute_multirange([i.vert_range for i in domains])
    return Domain(horz_range, vert_range)

def expand_domain(domain: Domain, factor: float):
    horz_range = expand_range(domain.horz_range, factor)
    vert_range = expand_range(domain.vert_range, factor)
    return Domain(horz_range, vert_range)

def calculate_cardinal_domain(
    domains: list[Domain], cardinal_expansion_factor: float = 1.1
):
    total_domain = compute_multidomain(domains)
    cardinal_domain = expand_domain(total_domain, cardinal_expansion_factor)
    return cardinal_domain
