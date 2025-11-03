from datetime import time, timedelta
t = time(hour=0, minute=0)
t
td = timedelta(minute=45)
td = timedelta(minutes=45)
td
td*4
td + t
help(td)
from datetime import datetime 
mydt = datetime(2021, 1, 1, 0, 0)
mydt + td
j = mydt + td
j.time
j.time()
mydate = date(2025, 1,1)
from datetime import date 
mydate = date(2025, 1,1)
jj = datetime.combine(mydate, t)
jj
jj + td
help 
help()
td = timedelta(minutes=45)
td.seconds // 60
td*4
tbef = time(23, 42)
tafter = time(0, 12)
tmidnight = time(0,0)
tafter > tmidnight
tpremid = time(23, 59)
tafter > tpremid
tbef < tmid
tbef < tmidnight
time(23, 53)
ttest = time(23, 53)
ttest >= tmi
ttest >= tmidnight
60 //4
60 / 4
60 // 2
help()
from datetime import time 
from datetime import datetime
from datetime import datetime, date
FAKE_DATE = date(2025, 01, 01)
FAKE_DATE = date(2025, 1, 1)
stime = time(0,0)
etime = time(23, 59)
xr
import xarray as xr
xr.date_range(datetime.combine(FAKE_DATE, stime), datetime.combine(FAKE_DATE, etime))
xr.date_range(datetime.combine(FAKE_DATE, stime), datetime.combine(FAKE_DATE, etime), freq="min")
tix = xr.date_range(datetime.combine(FAKE_DATE, stime), datetime.combine(FAKE_DATE, etime), freq="min")
len(tix)
tix.sel(tix.time=stime)
tix.sel(tix.time==stime)
ds = xr.Dataset({"foo": ("time", np.arange(365 * 24)), "time": tix})
import numpy as np 
ds = xr.Dataset({"foo": ("time", np.arange(60 * 24)), "time": tix})
ds
ds.sel(time=stime)
ds.sel(time=etime)
ds.sel(time.time=time)
ds.sel(time.time==time)
ds = xr.Dataset({"foo": ("time", np.arange(60 * 24)), "datetime": tix})
ds.sel(datetime.dt.time==time)
ds.sel(datetime.time==time)
ds.datetime.dt
ds.datetime.dt.time
ds.sel(ds.datetime.dt.time==etime)
ds.isel(ds.datetime.dt.time==etime)
ds.isel(time=(ds.datetime.dt.time==etime))
ds.isel(datetime=(ds.datetime.dt.time==etime))
ds.isel(datetime=(ds.datetime.dt.time==etime)).values
ds.isel(foo=(ds.datetime.dt.time==etime)).values
ds
ds = xr.DataArray(np.zeros(shape=(60*24)), coords={"datetime":tix})
ds
ds.dims
ds.isel(datetime=(ds.datetime.dt.time==etime)).values
ds.isel(ds.datetime.dt.time==etime).values
ds.sel(ds.datetime.dt.time==etime).values
ds.sel(datetime=slice(stime, 

)

mtime = time(13,15)
ds.sel(datetime=slice(stime, mtime))
ds.sel(datetime.dt.time=slice(stime, mtime))
ds.isel(datetime=(datetime.dt.time==slice(stime, mtime)))
ds.isel(datetime=(ds.datetime.dt.time==slice(stime, mtime)))
ds.sel(datetime=slice(stime, mtime), method="nearest")
ds.sel(datetime=slice(datetime.combine(FAKE_DATE, stime),datetime.combine(FAKE_DATE, mtime)), method="nearest")
ds.sel(datetime=slice(datetime.combine(FAKE_DATE, stime),datetime.combine(FAKE_DATE, mtime)))
