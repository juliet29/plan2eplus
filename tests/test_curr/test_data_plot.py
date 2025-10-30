from replan2eplus.ex.make import make_data_plot
from replan2eplus.paths import DynamicPaths, ep_paths
from replan2eplus.ex.afn import AFNExampleCases


def test_make_data_plot():
    path = DynamicPaths.afn_examples / AFNExampleCases.A_ew.name
    dp = make_data_plot(path)
    dp.show()


if __name__ == "__main__":
    test_make_data_plot()
