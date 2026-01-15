from cyclopts import App
from rich.pretty import pretty_repr
from loguru import logger

from replan2eplus.ex.make import make_test_case
from replan2eplus.ex.afn import AFNEdgeGroups as AFNEdgeGroups

studies_app = App(name="studies")


@studies_app.command()
def study_case():
    case = make_test_case(AFNEdgeGroups.A_ew)
    logger.info(pretty_repr(case.objects))
