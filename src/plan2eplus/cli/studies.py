from cyclopts import App
from loguru import logger
from omegaconf import OmegaConf

from plan2eplus.ex.make import make_test_case
from plan2eplus.ex.afn import AFNEdgeGroups as AFNEdgeGroups
from plan2eplus.paths import BASE_PATH
from plan2eplus.ep_paths import EpConfig, EpPaths

studies_app = App(name="studies")


@studies_app.command()
def study_case():
    case = make_test_case(AFNEdgeGroups.A_ew)
    zone_names = [i.zone_name for i in case.objects.zones]
    logger.info(zone_names)


@studies_app.command()
def try_config():
    schema = OmegaConf.structured(EpConfig)
    config_path = BASE_PATH / "config/test.yaml"
    user_path = BASE_PATH / "config/user.yaml"
    conf = OmegaConf.load(config_path)
    user_conf = OmegaConf.load(user_path)
    # the later config takes precednece..
    res = OmegaConf.merge(schema, conf, user_conf)
    print(OmegaConf.to_yaml(res))
    return res


@studies_app.command()
def try_epath():
    epath = EpPaths()
    print(epath.material_idfs)
