from plan2eplus.results.sql import create_result_for_qoi, get_sql_results
from rich import print as rprint
import pytest
import numpy as np

pytest.skip(allow_module_level=True)
# TODO: clean tests..


def get_results():
    # case = ExistCase(PATH_TO_IDD, TWO_ROOM_RESULTS / "out.idf")
    sql = get_sql_results(TWO_ROOM_RESULTS)
    return create_result_for_qoi(sql, "Zone Mean Air Temperature")


def get_qoi(qoi: OutputVariables):
    sql = get_sql_results(TWO_ROOM_RESULTS)
    return create_result_for_qoi(sql, qoi)


# TODO test selecting times


def test_get_results():
    sql = get_sql_results(TWO_ROOM_RESULTS)
    qoi_result = create_result_for_qoi(sql, "Zone Mean Air Temperature")
    # qoi_result = QOIResult.from_sql_collections(test_collections)
    # rprint(qoi_result.data_arr.to_dict())
    assert qoi_result.data_arr.shape == (96, 2)


def test_add_qois():
    flow12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate")
    flow21 = get_qoi("AFN Linkage Node 2 to Node 1 Volume Flow Rate")
    new_qoi = flow12 + flow21
    xarr_val = flow12.data_arr + flow21.data_arr
    assert xarr_val.equals(new_qoi.data_arr)


def test_bad_add_qois():
    flow12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate")
    not_a_flow = get_qoi("Zone Mean Air Temperature")
    with pytest.raises(AssertionError):
        _ = flow12 + not_a_flow


@pytest.mark.xfail()
def test_select_instant():
    exoected_result = [0.07208911, 0.0]
    flow12 = get_qoi("AFN Linkage Node 1 to Node 2 Volume Flow Rate")
    # dates = flow12.data_arr.datetimes.dt.hour

    res = flow12.data_arr.isel(datetimes=(flow12.data_arr.datetimes.dt.hour == 12))
    res2 = res.isel(datetimes=(res.datetimes.dt.minute == 0))[0]
    rprint(res)
    rprint(res2)
    rprint(res2.values[0])
    assert np.isclose(res2.values[0], exoected_result[0])


if __name__ == "__main__":
    test_select_instant()
