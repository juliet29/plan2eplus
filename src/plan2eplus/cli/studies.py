from cyclopts import App
from loguru import logger

from plan2eplus.ex.make import make_test_case
from plan2eplus.ex.afn import AFNEdgeGroups as AFNEdgeGroups

studies_app = App(name="studies")


@studies_app.command()
def study_case():
    case = make_test_case(AFNEdgeGroups.A_ew)
    zone_names = [i.zone_name for i in case.objects.zones]
    logger.info(zone_names)
