import numpy as np
import xarray as xr
from rich import print as rprint

# from plan2eplus.ops.schedules.interfaces.day import xarray_day

data = np.array([[10.0, 0.0], [11.0, 1.0], [12.0, 2.0]])
rooms = ["room1", "room2"]
times = [0, 1, 2]
coords = [times, rooms]
dims = ["time", "room"]


def xarr_w_dims():
    """
    <xarray.DataArray (time: 3, room: 2)> Size: 48B
    array([[10.,  0.],
           [11.,  1.],
           [12.,  2.]])
    Coordinates:
      * time     (time) int64 24B 0 1 2
      * room     (room) <U5 40B 'room1' 'room2'
    """
    xarr = xr.DataArray(data, coords=coords, dims=dims)
    print(xarr)


def xarr_no_dims():
    """
    <xarray.DataArray (dim_0: 3, dim_1: 2)> Size: 48B
    array([[10.,  0.],
           [11.,  1.],
           [12.,  2.]])
    Coordinates:
      * dim_0    (dim_0) int64 24B 0 1 2
      * dim_1    (dim_1)  <U5 40B 'room1' 'room2'
    """
    xarr = xr.DataArray(data, coords=coords)
    print(xarr)


def adding_two_arrays_attrs():
    attrs1 = {"qoi": "qoi1", "unit": "unit1"}
    attrs2 = {"qoi": "qoi2", "unit": "unit1"}
    xarr1 = xr.DataArray(data, coords=coords, dims=dims, attrs=attrs1)
    xarr2 = xr.DataArray(data * 2, coords=coords, dims=dims, attrs=attrs2)
    with xr.set_options(keep_attrs=True):
        xarr3 = xarr1 + xarr2
        rprint(xarr1)
        rprint(xarr3)


def adding_two_arrays():
    xarr1 = xr.DataArray(data, coords=coords, dims=dims)
    xarr2 = xr.DataArray(data * 2, coords=coords, dims=dims)

    xarr3 = xarr1 + xarr2

    # print(xarr3)

    # # indexing..
    # print(xarr3.loc[:, "room1"])
    # print(xarr3.sel(room="room1"))
    # print(xarr3.sel(time=0))

    # # aggregating..
    # print(xarr3.sum(dim=["time"]))

    # print(xarr3.data)
    rprint(xarr3.to_dict())
    # pd_df = xarr3.to_dataframe(name="test")
    # rprint(pd_df)
    # rprint(pl.from_pandas(data=pd_df, include_index=True))


def test_reorient_numpy_arr():
    arr = np.array([[1, 2, 3], [11, 12, 13]])
    rprint(arr)
    rprint(np.transpose(arr))


def access():
    xarr1 = xr.DataArray(data, coords=coords, dims=dims)
    print(xarr1.dims)
    print(xarr1.coords["time"].values)


if __name__ == "__main__":
    # adding_two_arrays_attrs()
    pass
