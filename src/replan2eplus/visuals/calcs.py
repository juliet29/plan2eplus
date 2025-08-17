from replan2eplus.geometry.domain import Domain
from matplotlib.patches import Rectangle


def domain_to_mpl_patch(domain: Domain):
    return Rectangle(
        (domain.horz_range.min, domain.vert_range.min),
        domain.horz_range.size,
        domain.vert_range.size,
        fill=False,
    )
