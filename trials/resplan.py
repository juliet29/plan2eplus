from replan2eplus.ezcase.ez import EZ
from rich.pretty import pprint
from replan2eplus.paths import DynamicPaths, ep_paths


def study_resplan():
    path = DynamicPaths.trials / "001"
    idf_path = path / ep_paths.idf_name

    case = EZ(idf_path=idf_path, output_path=path, read_existing=True)
    pprint(case.objects.zones)
    # make_base_plot(case)
    # case.save_and_run(
    #     save=True, epw_path=ep_paths.default_weather, run=True, output_path=path
    # )


if __name__ == "__main__":
    study_resplan()
