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

    "ndarray": _cast(np.array([1, 2, 3, 4]), lambda d: d.tolist()),

    "pdSeries": pd.Series([10, 20, 30]),

    "pdDataframe": pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": ["a", "b", "c"]
    }),

    "dict": {"key1": "value1", "key2": 42},

    "datetime": datetime.datetime(2025, 1, 1, 12, 0, 0, tzinfo=datetime.UTC),

    "date": datetime.date(2025, 1, 1),

    "time": datetime.time(14, 30, 15),

    "timedelta": datetime.timedelta(days=2, hours=3, minutes=15),

    "pdTimestamp": pd.Timestamp("2025-01-01 12:00:00"),

    "pdTimedelta": pd.Timedelta(days=5, minutes=45),

    "pdPeriod": pd.Period("2025-03", freq="M"),

    "pdInterval": pd.Interval(0, 10, closed="both"),

    "npint32": np.int32(42),

    "npfloat64": np.float64(3.14159),

    "npdatetime64": np.datetime64("2025-01-01T12:00:00"),

    "nptimedelta64": np.timedelta64(3, "D"),

    "decimalDecimal": decimal.Decimal("12.34"),

    "fraction": fractions.Fraction(3, 7),

    "uuid": _cast(uuid.UUID("12345678123456781234567812345678"), str),

    "pathlibPath": pathlib.Path("/path/example.txt"),

    "pdCategorical": pd.Categorical(["apple", "banana", "apple"]),

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
}

