from replan2eplus.ex.make import make_data_plot
from replan2eplus.visuals.data.data_plot import handle_external_node_data
from replan2eplus.paths import DynamicPaths, ep_paths
from replan2eplus.ex.afn import AFNExampleCases

from replan2eplus.results.sql import get_qoi
from replan2eplus.ezcase.ez import EZ, ep_paths


def test_make_data_plot():
    path = DynamicPaths.afn_examples / AFNExampleCases.A_ew.name
    dp = make_data_plot(path, hour=1)
    # dp.show()
    assert 1
    return dp


def test_handle_external_node_data():
    path = DynamicPaths.afn_examples / AFNExampleCases.A_ns.name
    # dp.show()
    hour = 12
    case = EZ(idf_path=path / ep_paths.idf_name)
    pressure = get_qoi("AFN Node Total Pressure", path)
    data_at_noon = pressure.select_time(hour)
    handle_external_node_data(data_at_noon)


if __name__ == "__main__":
    dp = test_make_data_plot()
    dp.show()
    # test_handle_external_node_data()
