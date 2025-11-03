from datetime import time, timedelta
t = time(hour=0, minute=0)
t
# OUT: datetime.time(0, 0)
td = timedelta(minute=45)
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     td = timedelta(minute=45)
# OUT: TypeError: __new__() got an unexpected keyword argument 'minute'. Did you mean 'minutes'?
td = timedelta(minutes=45)
td
# OUT: datetime.timedelta(seconds=2700)
td*4
# OUT: datetime.timedelta(seconds=10800)
td + t
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     td + t
# OUT:     ~~~^~~
# OUT: TypeError: unsupported operand type(s) for +: 'datetime.timedelta' and 'datetime.time'
help(td)
from datetime import datetime 
mydt = datetime(2021, 1, 1, 0, 0)
mydt + td
# OUT: datetime.datetime(2021, 1, 1, 0, 45)
j = mydt + td
j.time
# OUT: <built-in method time of datetime.datetime object at 0x105b42790>
j.time()
# OUT: datetime.time(0, 45)
mydate = date(2025, 1,1)
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     mydate = date(2025, 1,1)
# OUT:              ^^^^
# OUT: NameError: name 'date' is not defined
from datetime import date 
mydate = date(2025, 1,1)
jj = datetime.combine(mydate, t)
jj
# OUT: datetime.datetime(2025, 1, 1, 0, 0)
jj + td
# OUT: datetime.datetime(2025, 1, 1, 0, 45)
help 
# OUT: Type help() for interactive help, or help(object) for help about object.
help()
# OUT: Welcome to Python 3.13's help utility! If this is your first time using
# OUT: Python, you should definitely check out the tutorial at
# OUT: https://docs.python.org/3.13/tutorial/.
# OUT: Enter the name of any module, keyword, or topic to get help on writing
# OUT: Python programs and using Python modules.  To get a list of available
# OUT: modules, keywords, symbols, or topics, enter "modules", "keywords",
# OUT: "symbols", or "topics".
# OUT: Each module also comes with a one-line summary of what it does; to list
# OUT: the modules whose name or summary contain a given string such as "spam",
# OUT: enter "modules spam".
# OUT: To quit this help utility and return to the interpreter,
# OUT: enter "q", "quit" or "exit".
# OUT: You are now leaving help and returning to the Python interpreter.
# OUT: If you want to ask for help on a particular object directly from the
# OUT: interpreter, you can type "help(object)".  Executing "help('string')"
# OUT: has the same effect as typing a particular string at the help> prompt.
td = timedelta(minutes=45)
td.seconds // 60
# OUT: 45
td*4
# OUT: datetime.timedelta(seconds=10800)
tbef = time(23, 42)
tafter = time(0, 12)
tmidnight = time(0,0)
tafter > tmidnight
# OUT: True
tpremid = time(23, 59)
tafter > tpremid
# OUT: False
tbef < tmid
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     tbef < tmid
# OUT:            ^^^^
# OUT: NameError: name 'tmid' is not defined
tbef < tmidnight
# OUT: False
time(23, 53)
# OUT: datetime.time(23, 53)
ttest = time(23, 53)
ttest >= tmi
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ttest >= tmi
# OUT:              ^^^
# OUT: NameError: name 'tmi' is not defined
ttest >= tmidnight
# OUT: True
60 //4
# OUT: 15
60 / 4
# OUT: 15.0
60 // 2
# OUT: 30
help()
# OUT: Welcome to Python 3.13's help utility! If this is your first time using
# OUT: Python, you should definitely check out the tutorial at
# OUT: https://docs.python.org/3.13/tutorial/.
# OUT: Enter the name of any module, keyword, or topic to get help on writing
# OUT: Python programs and using Python modules.  To get a list of available
# OUT: modules, keywords, symbols, or topics, enter "modules", "keywords",
# OUT: "symbols", or "topics".
# OUT: Each module also comes with a one-line summary of what it does; to list
# OUT: the modules whose name or summary contain a given string such as "spam",
# OUT: enter "modules spam".
# OUT: To quit this help utility and return to the interpreter,
# OUT: enter "q", "quit" or "exit".
# OUT: Please wait a moment while I gather a list of all available modules...
# OUT: test_sqlite3: testing with SQLite version 3.49.1
# OUT: /opt/homebrew/Cellar/python@3.13/3.13.2/Frameworks/Python.framework/Versions/3.13/lib/python3.13/pkgutil.py:78: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
# OUT:   __import__(info.name)
# OUT: 30fcd23745efe32ce681__mypyc _thread             grp                 quopri
# OUT: PIL                 _threading_local    gzip                random
# OUT: __future__          _tkinter            hashlib             re
# OUT: __hello__           _tokenize           heapq               readline
# OUT: __phello__          _tracemalloc        hmac                replan2eplus
# OUT: _abc                _typing             html                reprlib
# OUT: _aix_support        _uuid               http                requests
# OUT: _android_support    _virtualenv         idlelib             resource
# OUT: _apple_support      _warnings           idna                rich
# OUT: _ast                _weakref            imaplib             rlcompleter
# OUT: _asyncio            _weakrefset         importlib           runpy
# OUT: _bisect             _xxtestfuzz         iniconfig           sched
# OUT: _black_version      _zoneinfo           inspect             scipy
# OUT: _blake2             abc                 io                  secrets
# OUT: _bz2                activate_this       ipaddress           select
# OUT: _codecs             annotated_types     itertools           selectors
# OUT: _codecs_cn          antigravity         json                setuptools
# OUT: _codecs_hk          argparse            keyword             shapely
# OUT: _codecs_iso2022     array               kiwisolver          shelve
# OUT: _codecs_jp          ast                 ladybug             shlex
# OUT: _codecs_kr          asyncio             ladybug_geometry    shutil
# OUT: _codecs_tw          atexit              libfuturize         signal
# OUT: _collections        base64              libpasteurize       site
# OUT: _collections_abc    bdb                 linecache           sitecustomize
# OUT: _colorize           binascii            locale              six
# OUT: _compat_pickle      bisect              logging             smtplib
# OUT: _compression        black               loguru              socket
# OUT: _contextvars        blackd              lxml                socketserver
# OUT: _csv                blessed             lzma                soupsieve
# OUT: _ctypes             blib2to3            mailbox             sqlite3
# OUT: _ctypes_test        bpdb                markdown_it         sre_compile
# OUT: _curses             bpython             marshal             sre_constants
# OUT: _curses_panel       bs4                 math                sre_parse
# OUT: _datetime           builtins            matplotlib          ssl
# OUT: _dbm                bz2                 mdurl               stat
# OUT: _decimal            cProfile            mimetypes           statistics
# OUT: _distutils_hack     calendar            mmap                string
# OUT: _elementtree        certifi             modulefinder        stringprep
# OUT: _functools          charset_normalizer  multiprocessing     struct
# OUT: _hashlib            click               munch               subprocess
# OUT: _heapq              cmath               mypy                symtable
# OUT: _imp                cmd                 mypy_extensions     sys
# OUT: _interpchannels     code                mypyc               sysconfig
# OUT: _interpqueues       codecs              netrc               syslog
# OUT: _interpreters       codeop              networkx            tabnanny
# OUT: _io                 collections         ntpath              tabulate
# OUT: _ios_support        colorsys            nturl2path          tarfile
# OUT: _json               compileall          numbers             tempfile
# OUT: _locale             concurrent          numpy               termios
# OUT: _lsprof             configparser        opcode              test
# OUT: _lzma               contextlib          operator            tests
# OUT: _markupbase         contextvars         optparse            textwrap
# OUT: _md5                contourpy           os                  this
# OUT: _multibytecodec     copy                packaging           threading
# OUT: _multiprocessing    copyreg             pandas              time
# OUT: _opcode             coverage            past                timeit
# OUT: _opcode_metadata    csv                 pathlib             tinynumpy
# OUT: _operator           ctypes              pathspec            tkinter
# OUT: _osx_support        curses              pdb                 token
# OUT: _pickle             curtsies            pickle              tokenize
# OUT: _posixshmem         cwcwidth            pickletools         tomli_w
# OUT: _posixsubprocess    cycler              pipe                tomllib
# OUT: _py_abc             dataclasses         pkg_resources       trace
# OUT: _pydatetime         datetime            pkgutil             traceback
# OUT: _pydecimal          dateutil            platform            tracemalloc
# OUT: _pyio               dbm                 platformdirs        transforms3d
# OUT: _pylong             decimal             plistlib            tty
# OUT: _pyrepl             decorator           pluggy              turtle
# OUT: _pytest             difflib             polars              turtledemo
# OUT: _queue              dis                 pooch               types
# OUT: _random             doctest             poplib              typing
# OUT: _scproxy            dot_parser          posix               typing_extensions
# OUT: _sha1               dotenv              posixpath           typing_inspection
# OUT: _sha2               edfc647aaf02b20aa651__mypyc pprint              tzdata
# OUT: _sha3               email               profile             unicodedata
# OUT: _signal             encodings           pstats              unittest
# OUT: _sitebuiltins       ensurepip           pty                 urllib
# OUT: _socket             enum                pwd                 urllib3
# OUT: _sqlite3            eppy                py                  utils4plans
# OUT: _sre                errno               py_compile          uuid
# OUT: _ssl                expression          pyarrow             venv
# OUT: _stat               faulthandler        pyclbr              warnings
# OUT: _statistics         fcntl               pyclipper           wave
# OUT: _string             filecmp             pydantic            wcwidth
# OUT: _strptime           fileinput           pydantic_core       weakref
# OUT: _struct             fnmatch             pydantic_settings   webbrowser
# OUT: _suggestions        fontTools           pydoc               whenever
# OUT: _symtable           fractions           pydoc_data          wsgiref
# OUT: _sysconfig          ftplib              pydot               xarray
# OUT: _sysconfigdata__darwin_darwin functools           pyexpat             xdg
# OUT: _testbuffer         future              pygments            xml
# OUT: _testcapi           gc                  pylab               xmlrpc
# OUT: _testclinic         genericpath         pyparsing           xxlimited
# OUT: _testclinic_limited geomeppy            pypoly2tri          xxlimited_35
# OUT: _testexternalinspection getopt              pyprojroot          xxsubtype
# OUT: _testimportmultiple getpass             pytest              zipapp
# OUT: _testinternalcapi   gettext             pytest_cov          zipfile
# OUT: _testlimitedcapi    glob                pytest_skip_slow    zipimport
# OUT: _testmultiphase     graphlib            pytz                zlib
# OUT: _testsinglephase    greenlet            queue               zoneinfo
# OUT: Enter any module name to get more help.  Or, type "modules spam" to search
# OUT: for modules whose name or summary contain the string "spam".
# OUT: Here is a list of the punctuation symbols which Python assigns special meaning
# OUT: to. Enter any symbol to get more help.
# OUT: !=                  +                   <<=                 _
# OUT: "                   +=                  <=                  __
# OUT: """                 ,                   <>                  `
# OUT: %                   -                   ==                  b"
# OUT: %=                  -=                  >                   b'
# OUT: &                   .                   >=                  f"
# OUT: &=                  ...                 >>                  f'
# OUT: '                   /                   >>=                 j
# OUT: '''                 //                  @                   r"
# OUT: (                   //=                 J                   r'
# OUT: )                   /=                  [                   u"
# OUT: *                   :                   \                   u'
# OUT: **                  :=                  ]                   |
# OUT: **=                 <                   ^                   |=
# OUT: *=                  <<                  ^=                  ~
# OUT: You are now leaving help and returning to the Python interpreter.
# OUT: If you want to ask for help on a particular object directly from the
# OUT: interpreter, you can type "help(object)".  Executing "help('string')"
# OUT: has the same effect as typing a particular string at the help> prompt.
from datetime import time 
from datetime import datetime
from datetime import datetime, date
FAKE_DATE = date(2025, 01, 01)
# OUT:   File "<input>", line 1
# OUT:     FAKE_DATE = date(2025, 01, 01)
# OUT:                            ^
# OUT: SyntaxError: leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers
FAKE_DATE = date(2025, 1, 1)
stime = time(0,0)
etime = time(23, 59)
xr
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     xr
# OUT: NameError: name 'xr' is not defined
import xarray as xr
xr.date_range(datetime.combine(FAKE_DATE, stime), datetime.combine(FAKE_DATE, etime))
# OUT: DatetimeIndex(['2025-01-01'], dtype='datetime64[ns]', freq='D')
xr.date_range(datetime.combine(FAKE_DATE, stime), datetime.combine(FAKE_DATE, etime), freq="min")
# OUT: DatetimeIndex(['2025-01-01 00:00:00', '2025-01-01 00:01:00',
# OUT:                '2025-01-01 00:02:00', '2025-01-01 00:03:00',
# OUT:                '2025-01-01 00:04:00', '2025-01-01 00:05:00',
# OUT:                '2025-01-01 00:06:00', '2025-01-01 00:07:00',
# OUT:                '2025-01-01 00:08:00', '2025-01-01 00:09:00',
# OUT:                ...
# OUT:                '2025-01-01 23:50:00', '2025-01-01 23:51:00',
# OUT:                '2025-01-01 23:52:00', '2025-01-01 23:53:00',
# OUT:                '2025-01-01 23:54:00', '2025-01-01 23:55:00',
# OUT:                '2025-01-01 23:56:00', '2025-01-01 23:57:00',
# OUT:                '2025-01-01 23:58:00', '2025-01-01 23:59:00'],
# OUT:               dtype='datetime64[ns]', length=1440, freq='min')
tix = xr.date_range(datetime.combine(FAKE_DATE, stime), datetime.combine(FAKE_DATE, etime), freq="min")
len(tix)
# OUT: 1440
tix.sel(tix.time=stime)
# OUT:   File "<input>", line 1
# OUT:     tix.sel(tix.time=stime)
# OUT:             ^^^^^^^^^
# OUT: SyntaxError: expression cannot contain assignment, perhaps you meant "=="?
tix.sel(tix.time==stime)
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     tix.sel(tix.time==stime)
# OUT:     ^^^^^^^
# OUT: AttributeError: 'DatetimeIndex' object has no attribute 'sel'
ds = xr.Dataset({"foo": ("time", np.arange(365 * 24)), "time": tix})
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds = xr.Dataset({"foo": ("time", np.arange(365 * 24)), "time": tix})
# OUT:                                      ^^
# OUT: NameError: name 'np' is not defined
import numpy as np 
ds = xr.Dataset({"foo": ("time", np.arange(60 * 24)), "time": tix})
ds
# OUT: <xarray.Dataset> Size: 23kB
# OUT: Dimensions:  (time: 1440)
# OUT: Coordinates:
# OUT:   * time     (time) datetime64[ns] 12kB 2025-01-01 ... 2025-01-01T23:59:00
# OUT: Data variables:
# OUT:     foo      (time) int64 12kB 0 1 2 3 4 5 6 ... 1434 1435 1436 1437 1438 1439
ds.sel(time=stime)
# OUT: <xarray.Dataset> Size: 16B
# OUT: Dimensions:  (time: 1)
# OUT: Coordinates:
# OUT:   * time     (time) datetime64[ns] 8B 2025-01-01
# OUT: Data variables:
# OUT:     foo      (time) int64 8B 0
ds.sel(time=etime)
# OUT: <xarray.Dataset> Size: 16B
# OUT: Dimensions:  (time: 1)
# OUT: Coordinates:
# OUT:   * time     (time) datetime64[ns] 8B 2025-01-01T23:59:00
# OUT: Data variables:
# OUT:     foo      (time) int64 8B 1439
ds.sel(time.time=time)
# OUT:   File "<input>", line 1
# OUT:     ds.sel(time.time=time)
# OUT:            ^^^^^^^^^^
# OUT: SyntaxError: expression cannot contain assignment, perhaps you meant "=="?
ds.sel(time.time==time)
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.sel(time.time==time)
# OUT:            ^^^^^^^^^
# OUT: AttributeError: type object 'datetime.time' has no attribute 'time'
ds = xr.Dataset({"foo": ("time", np.arange(60 * 24)), "datetime": tix})
ds.sel(datetime.dt.time==time)
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.sel(datetime.dt.time==time)
# OUT:            ^^^^^^^^^^^
# OUT: AttributeError: type object 'datetime.datetime' has no attribute 'dt'. Did you mean: 'dst'?
ds.sel(datetime.time==time)
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.sel(datetime.time==time)
# OUT:     ~~~~~~^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2973, in sel
# OUT:     indexers = either_dict_or_kwargs(indexers, indexers_kwargs, "sel")
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/namedarray/utils.py", line 190, in either_dict_or_kwargs
# OUT:     raise ValueError(f"the first argument to .{func_name} must be a dictionary")
# OUT: ValueError: the first argument to .sel must be a dictionary
ds.datetime.dt
# OUT: <xarray.core.accessor_dt.DatetimeAccessor object at 0x1443c68d0>
ds.datetime.dt.time
# OUT: <xarray.DataArray 'time' (datetime: 1440)> Size: 12kB
# OUT: array([datetime.time(0, 0), datetime.time(0, 1), datetime.time(0, 2), ...,
# OUT:        datetime.time(23, 57), datetime.time(23, 58),
# OUT:        datetime.time(23, 59)], shape=(1440,), dtype=object)
# OUT: Coordinates:
# OUT:   * datetime  (datetime) datetime64[ns] 12kB 2025-01-01 ... 2025-01-01T23:59:00
ds.sel(ds.datetime.dt.time==etime)
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.sel(ds.datetime.dt.time==etime)
# OUT:     ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2973, in sel
# OUT:     indexers = either_dict_or_kwargs(indexers, indexers_kwargs, "sel")
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/namedarray/utils.py", line 184, in either_dict_or_kwargs
# OUT:     if pos_kwargs is None or pos_kwargs == {}:
# OUT:                              ^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/common.py", line 155, in __bool__
# OUT:     return bool(self.values)
# OUT: ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
ds.isel(ds.datetime.dt.time==etime)
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.isel(ds.datetime.dt.time==etime)
# OUT:     ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2819, in isel
# OUT:     indexers = either_dict_or_kwargs(indexers, indexers_kwargs, "isel")
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/namedarray/utils.py", line 184, in either_dict_or_kwargs
# OUT:     if pos_kwargs is None or pos_kwargs == {}:
# OUT:                              ^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/common.py", line 155, in __bool__
# OUT:     return bool(self.values)
# OUT: ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
ds.isel(time=(ds.datetime.dt.time==etime))
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.isel(time=(ds.datetime.dt.time==etime))
# OUT:     ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2821, in isel
# OUT:     return self._isel_fancy(indexers, drop=drop, missing_dims=missing_dims)
# OUT:            ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2877, in _isel_fancy
# OUT:     new_var = var.isel(indexers=var_indexers)
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/variable.py", line 1130, in isel
# OUT:     return self[key]
# OUT:            ~~~~^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/variable.py", line 817, in __getitem__
# OUT:     dims, indexer, new_order = self._broadcast_indexes(key)
# OUT:                                ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/variable.py", line 656, in _broadcast_indexes
# OUT:     self._validate_indexers(key)
# OUT:     ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/variable.py", line 716, in _validate_indexers
# OUT:     raise IndexError(
# OUT:     ...<3 lines>...
# OUT:     )
# OUT: IndexError: Boolean indexer should be unlabeled or on the same dimension to the indexed array. Indexer is on ('datetime',) but the target dimension is time.
ds.isel(datetime=(ds.datetime.dt.time==etime))
# OUT: <xarray.Dataset> Size: 12kB
# OUT: Dimensions:   (time: 1440, datetime: 1)
# OUT: Coordinates:
# OUT:   * datetime  (datetime) datetime64[ns] 8B 2025-01-01T23:59:00
# OUT: Dimensions without coordinates: time
# OUT: Data variables:
# OUT:     foo       (time) int64 12kB 0 1 2 3 4 5 6 ... 1434 1435 1436 1437 1438 1439
ds.isel(datetime=(ds.datetime.dt.time==etime)).values
# OUT: <bound method Mapping.values of <xarray.Dataset> Size: 12kB
# OUT: Dimensions:   (time: 1440, datetime: 1)
# OUT: Coordinates:
# OUT:   * datetime  (datetime) datetime64[ns] 8B 2025-01-01T23:59:00
# OUT: Dimensions without coordinates: time
# OUT: Data variables:
# OUT:     foo       (time) int64 12kB 0 1 2 3 4 5 6 ... 1434 1435 1436 1437 1438 1439>
ds.isel(foo=(ds.datetime.dt.time==etime)).values
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.isel(foo=(ds.datetime.dt.time==etime)).values
# OUT:     ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2821, in isel
# OUT:     return self._isel_fancy(indexers, drop=drop, missing_dims=missing_dims)
# OUT:            ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2864, in _isel_fancy
# OUT:     valid_indexers = dict(self._validate_indexers(indexers, missing_dims))
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2618, in _validate_indexers
# OUT:     indexers = drop_dims_from_indexers(indexers, self.dims, missing_dims)
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/utils.py", line 864, in drop_dims_from_indexers
# OUT:     raise ValueError(
# OUT:         f"Dimensions {invalid} do not exist. Expected one or more of {dims}"
# OUT:     )
# OUT: ValueError: Dimensions {'foo'} do not exist. Expected one or more of FrozenMappingWarningOnValuesAccess({'time': 1440, 'datetime': 1440})
ds
# OUT: <xarray.Dataset> Size: 23kB
# OUT: Dimensions:   (time: 1440, datetime: 1440)
# OUT: Coordinates:
# OUT:   * datetime  (datetime) datetime64[ns] 12kB 2025-01-01 ... 2025-01-01T23:59:00
# OUT: Dimensions without coordinates: time
# OUT: Data variables:
# OUT:     foo       (time) int64 12kB 0 1 2 3 4 5 6 ... 1434 1435 1436 1437 1438 1439
ds = xr.DataArray(np.zeros(shape=(60*24)), coords={"datetime":tix})
ds
# OUT: <xarray.DataArray (datetime: 1440)> Size: 12kB
# OUT: array([0., 0., 0., ..., 0., 0., 0.], shape=(1440,))
# OUT: Coordinates:
# OUT:   * datetime  (datetime) datetime64[ns] 12kB 2025-01-01 ... 2025-01-01T23:59:00
ds.dims
# OUT: ('datetime',)
ds.isel(datetime=(ds.datetime.dt.time==etime)).values
# OUT: array([0.])
ds.isel(ds.datetime.dt.time==etime).values
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.isel(ds.datetime.dt.time==etime).values
# OUT:     ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataarray.py", line 1570, in isel
# OUT:     indexers = either_dict_or_kwargs(indexers, indexers_kwargs, "isel")
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/namedarray/utils.py", line 184, in either_dict_or_kwargs
# OUT:     if pos_kwargs is None or pos_kwargs == {}:
# OUT:                              ^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/common.py", line 155, in __bool__
# OUT:     return bool(self.values)
# OUT: ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
ds.sel(ds.datetime.dt.time==etime).values
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.sel(ds.datetime.dt.time==etime).values
# OUT:     ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataarray.py", line 1716, in sel
# OUT:     ds = self._to_temp_dataset().sel(
# OUT:         indexers=indexers,
# OUT:     ...<3 lines>...
# OUT:         **indexers_kwargs,
# OUT:     )
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2973, in sel
# OUT:     indexers = either_dict_or_kwargs(indexers, indexers_kwargs, "sel")
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/namedarray/utils.py", line 184, in either_dict_or_kwargs
# OUT:     if pos_kwargs is None or pos_kwargs == {}:
# OUT:                              ^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/common.py", line 155, in __bool__
# OUT:     return bool(self.values)
# OUT: ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
ds.sel(datetime=slice(stime, 

)

mtime = time(13,15)
ds.sel(datetime=slice(stime, mtime))
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.sel(datetime=slice(stime, mtime))
# OUT:     ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataarray.py", line 1716, in sel
# OUT:     ds = self._to_temp_dataset().sel(
# OUT:         indexers=indexers,
# OUT:     ...<3 lines>...
# OUT:         **indexers_kwargs,
# OUT:     )
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2974, in sel
# OUT:     query_results = map_index_queries(
# OUT:         self, indexers=indexers, method=method, tolerance=tolerance
# OUT:     )
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/indexing.py", line 201, in map_index_queries
# OUT:     results.append(index.sel(labels, **options))
# OUT:                    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/indexes.py", line 835, in sel
# OUT:     indexer = _query_slice(self.index, label, coord_name, method, tolerance)
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/indexes.py", line 575, in _query_slice
# OUT:     raise KeyError(
# OUT:     ...<3 lines>...
# OUT:     )
# OUT: KeyError: "cannot represent labeled-based slice indexer for coordinate 'datetime' with a slice over integer positions; the index is unsorted or non-unique"
ds.sel(datetime.dt.time=slice(stime, mtime))
# OUT:   File "<input>", line 1
# OUT:     ds.sel(datetime.dt.time=slice(stime, mtime))
# OUT:            ^^^^^^^^^^^^^^^^^
# OUT: SyntaxError: expression cannot contain assignment, perhaps you meant "=="?
ds.isel(datetime=(datetime.dt.time==slice(stime, mtime)))
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.isel(datetime=(datetime.dt.time==slice(stime, mtime)))
# OUT:                       ^^^^^^^^^^^
# OUT: AttributeError: type object 'datetime.datetime' has no attribute 'dt'. Did you mean: 'dst'?
ds.isel(datetime=(ds.datetime.dt.time==slice(stime, mtime)))
# OUT: <xarray.DataArray (datetime: 0)> Size: 0B
# OUT: array([], dtype=float64)
# OUT: Coordinates:
# OUT:   * datetime  (datetime) datetime64[ns] 0B 
ds.sel(datetime=slice(stime, mtime), method="nearest")
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.sel(datetime=slice(stime, mtime), method="nearest")
# OUT:     ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataarray.py", line 1716, in sel
# OUT:     ds = self._to_temp_dataset().sel(
# OUT:         indexers=indexers,
# OUT:     ...<3 lines>...
# OUT:         **indexers_kwargs,
# OUT:     )
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2974, in sel
# OUT:     query_results = map_index_queries(
# OUT:         self, indexers=indexers, method=method, tolerance=tolerance
# OUT:     )
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/indexing.py", line 201, in map_index_queries
# OUT:     results.append(index.sel(labels, **options))
# OUT:                    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/indexes.py", line 835, in sel
# OUT:     indexer = _query_slice(self.index, label, coord_name, method, tolerance)
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/indexes.py", line 564, in _query_slice
# OUT:     raise NotImplementedError(
# OUT:         "cannot use ``method`` argument if any indexers are slice objects"
# OUT:     )
# OUT: NotImplementedError: cannot use ``method`` argument if any indexers are slice objects
ds.sel(datetime=slice(datetime.combine(FAKE_DATE, stime),datetime.combine(FAKE_DATE, mtime)), method="nearest")
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT:     ds.sel(datetime=slice(datetime.combine(FAKE_DATE, stime),datetime.combine(FAKE_DATE, mtime)), method="nearest")
# OUT:     ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataarray.py", line 1716, in sel
# OUT:     ds = self._to_temp_dataset().sel(
# OUT:         indexers=indexers,
# OUT:     ...<3 lines>...
# OUT:         **indexers_kwargs,
# OUT:     )
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/dataset.py", line 2974, in sel
# OUT:     query_results = map_index_queries(
# OUT:         self, indexers=indexers, method=method, tolerance=tolerance
# OUT:     )
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/indexing.py", line 201, in map_index_queries
# OUT:     results.append(index.sel(labels, **options))
# OUT:                    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/indexes.py", line 835, in sel
# OUT:     indexer = _query_slice(self.index, label, coord_name, method, tolerance)
# OUT:   File "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/.venv/lib/python3.13/site-packages/xarray/core/indexes.py", line 564, in _query_slice
# OUT:     raise NotImplementedError(
# OUT:         "cannot use ``method`` argument if any indexers are slice objects"
# OUT:     )
# OUT: NotImplementedError: cannot use ``method`` argument if any indexers are slice objects
ds.sel(datetime=slice(datetime.combine(FAKE_DATE, stime),datetime.combine(FAKE_DATE, mtime)))
# OUT: <xarray.DataArray (datetime: 796)> Size: 6kB
# OUT: array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT: ...
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
# OUT:        0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
# OUT: Coordinates:
# OUT:   * datetime  (datetime) datetime64[ns] 6kB 2025-01-01 ... 2025-01-01T13:15:00
### 