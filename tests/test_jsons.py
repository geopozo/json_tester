import datetime
import decimal
import fractions
import json
import math
import pathlib
import pprint
import uuid
from collections import OrderedDict, defaultdict, namedtuple

import msgspec
import numpy as np
import orjson
import pandas as pd
import pytest
import simplejson
import ujson

# -------------------------------------------------------------------
# Define a simple namedtuple for testing:
# -------------------------------------------------------------------
MyPoint = namedtuple("MyPoint", ["x", "y"]) # noqa: PYI024 namedtuple
# add in typing.NamedTuple too

# -------------------------------------------------------------------
# Example “data” dict including a broad range of types:
# -------------------------------------------------------------------
data = {
    "list_valid_floats": [1.0, 2.2, 2.5, -0.43, 0.32, 0.23],

    "list_invalid_floats": [float("-inf"), float("inf"), float("NaN")],

    "ndarray": np.array([1, 2, 3, 4]),

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

    "uuid": uuid.UUID("12345678123456781234567812345678"),

    "pathlibPath": pathlib.Path("/path/example.txt"),

    "pdCategorical": pd.Categorical(["apple", "banana", "apple"]),

    "bool": True,

    "none": None,

    "set": {1, 2, 3},

    "frozenset": frozenset({1, 2, 3}),

    "bytes": b"hello world",

    "bytearray": bytearray(b"hello world"),

    # "complex": complex(1, 2),

    # "range": range(5),

    "memoryview": memoryview(b"memory"),

    "orderedDict": OrderedDict([("a", 1), ("b", 2), ("c", 3)]),

    "defaultDict": defaultdict(lambda: "missing", {"x": 100, "y": 200}),

    "namedtuple": MyPoint(1, 2),

    # "regexPattern": re.compile(r"^\d{3}-\d{2}-\d{4}$"),

    # "ellipsis": ...,
}

def assert_almost_equal_with_nan(a, b, fail=None): # noqa: C901
    """Assert but allow NaN to be equal to NaN."""
    if not fail:
        def fail():
            raise AssertionError(f"{pprint.pformat(a)} != {pprint.pformat(b)}")

    if isinstance(a, float) and isinstance(b, float):
        if math.isnan(a) and math.isnan(b):
            return
        if math.isinf(a) and math.isinf(b) and (a > 0) == (b > 0):
            return
        if math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
            return
        fail()
    elif isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            fail()
        for (x, y) in zip(a, b, strict=True):
            assert_almost_equal_with_nan(x, y, fail=fail)
    elif isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            fail()
        for k in a:
            assert_almost_equal_with_nan(a[k], b[k], fail=fail)
    elif a != b:
        fail()

encoders = {
    "json": lambda data: json.dumps(data),
    "ujson": lambda data: ujson.dumps(data),
    "orjson": lambda data: orjson.dumps(data).decode("utf-8"),
    "simplejson": lambda data: simplejson.dumps(data, allow_nan=True),
    "msgspec": lambda data: msgspec.json.encode(data).decode("utf-8"),
}

decoders = {
    "json": lambda data: json.loads(data),
    "ujson": lambda data: ujson.loads(data),
    "orjson": lambda data: orjson.loads(data.encode("utf-8")),
    "simplejson": lambda data: simplejson.loads(data, allow_nan=True),
    "msgspec": lambda data: msgspec.json.decode(data, strict=False),
}



@pytest.mark.parametrize(
    ("package", "encode_fn"),
    encoders.items(),
    ids=encoders.keys(),
)
@pytest.mark.parametrize(
    ("data_type", "data"),
    data.items(),
    ids=data.keys(),
)
def test_encode(benchmark, package, encode_fn, data_type, data):
    """Test encoding."""
    _ = package # standard include
    benchmark.group=f"encoding_{data_type}"
    benchmark(encode_fn, data)

@pytest.mark.parametrize(
    ("package", "decode_fn"),
    decoders.items(),
    ids=decoders.keys(),
)
@pytest.mark.parametrize(
    ("data_type", "data"),
    data.items(),
    ids=data.keys(),
)
def test_decode(benchmark, package, decode_fn, data_type, data):
    """Test decoding and equalness."""
    benchmark.group=f"decoding_{data_type}"
    encoded = encoders[package](data)
    benchmark(decode_fn, encoded)

# assert_almost_equal_with_nan(data,
