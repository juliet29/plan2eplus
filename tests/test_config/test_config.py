from plan2eplus.ep_paths import EpPaths
from pathlib import Path

DEV_PATH = Path("/Applications/EnergyPlus-22-2-0")
PROD_PATH = Path("././../static/_01_inputs/local_ep_files/")


def test_dev_ep_paths(monkeypatch):

    monkeypatch.setenv("APP_ENV", "dev")
    ep_paths = EpPaths()
    assert ep_paths.config.path_to_ep_install == DEV_PATH


def test_prod_ep_paths(monkeypatch):
    monkeypatch.setenv("APP_ENV", "prod")
    ep_paths = EpPaths()
    assert ep_paths.config.path_to_ep_install == PROD_PATH


if __name__ == "__main__":
    pass
