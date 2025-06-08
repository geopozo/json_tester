import datetime
import decimal
import fractions
import pathlib
import re
import uuid
from collections import OrderedDict, defaultdict, namedtuple
from typing import Any, NamedTuple

import numpy as np
import pandas as pd

import data_generators as dg

class CodecPair(NamedTuple):
    """If encoding/deocidng is different."""
    input: Any
    output: Any

def _cast(data, fn):
    """Generate pair from data + function."""
    return CodecPair(data, fn(data))

# -------------------------------------------------------------------
# Example "data" dict including a broad range of types:
# -------------------------------------------------------------------
data = {
    "list_valid_floats": [1.0, 2.2, 2.5, -0.43, 0.32, 0.23],

    "list_invalid_floats": [float("-inf"), float("inf"), float("NaN")],

    "dict": {"key1": "value1", "key2": 42},

    "datetime": _cast(
        datetime.datetime(2025, 1, 1, 12, 0, 0, tzinfo=datetime.UTC),
        str
    ),

    "date": datetime.date(2025, 1, 1),

    "time": datetime.time(14, 30, 15),

    "timedelta": datetime.timedelta(days=2, hours=3, minutes=15),

    "pd_Series": pd.Series([10, 20, 30]),

    "pd_Series_uint16": pd.Series([1, 2, 3], dtype="uint16"),

    "pd_Series_float64": pd.Series([1.5, 2.5, 3.5], dtype="float64"),

    "pd_Dataframe": pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    }),

    "pd_Timestamp": pd.Timestamp("2025-01-01 12:00:00"),

    "pd_Timedelta": pd.Timedelta(days=5, minutes=45),

    "pd_Period": pd.Period("2025-03", freq="M"),

    "pd_Interval": pd.Interval(0, 10, closed="both"),

    "pd_Categorical": pd.Categorical(["apple", "banana", "apple"]),


    # NumPy numeric types
    "nd_ndarray": _cast(np.array([1, 2, 3, 4]), lambda d: d.tolist()),

    "np_uint8": np.uint8(255),
    "np_uint16": np.uint16(65535),
    "np_int16": np.int16(-32768),
    "np_int32": np.int32(-123456),
    "np_float32": np.float32(3.14),
    "np_float64": np.float64(2.71828),

    "np_datetime64": np.datetime64("2025-01-01T12:00:00"),

    "np_timedelta64": np.timedelta64(3, "D"),

    "decimal_Decimal": decimal.Decimal("12.34"),

    "fraction": fractions.Fraction(3, 7),

    "uuid": _cast(uuid.UUID("12345678123456781234567812345678"), str),

    "pathlib_Path": pathlib.Path("/path/example.txt"),

    "bool": True,

    "none": None,

    "set": {1, 2, 3},

    "frozenset": frozenset({1, 2, 3}),

    "bytes": b"hello world",

    "bytearray": bytearray(b"hello world"),

    "complex": complex(1, 2),

    "range": range(5),

    "memoryview": memoryview(b"memory"),

    "orderedDict": OrderedDict([("a", 1), ("b", 2), ("c", 3)]),

    "defaultDict": defaultdict(lambda: "missing", {"x": 100, "y": 200}),

    "namedtuple": namedtuple("MyPoint", ["x", "y"])(1, 2), # noqa: PYI024 namedtuple

    "regexPattern": re.compile(r"^\d{3}-\d{2}-\d{4}$"),

    "ellipsis": ...,


    "pilImage_I16": dg.gen_pil_data(),

    "struct_uint16": dg.gen_struct_data(),

    "h5py_uint16_array": dg.gen_h5py_data(),

    "astropy_fits_uint16_array": dg.gen_astropy_data(),

    "dask_uint16_array": dg.gen_dask_data(),

    "polars_uint16_dataframe": dg.gen_polars_data(),

    "xarray_uint16_dataarray": dg.gen_xarray_data()
}
