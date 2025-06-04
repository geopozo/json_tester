import json
import math
import pprint

import pytest

from data import data

packages = ["json"]
try:
    import msgspec
    packages.append("msgspec")
except ImportError:
    pass

try:
    import orjson
    packages.append("orjson")
except ImportError:
    pass

try:
    import simplejson
    packages.append("simplejson")
except ImportError:
    pass

try:
    import ujson
    packages.append("ujson")
except ImportError:
    pass


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
    "package",
    packages,
    ids=packages,
)
@pytest.mark.parametrize(
    ("data_type", "data"),
    data.items(),
    ids=data.keys(),
)
def test_encode(benchmark, package, data_type, data):
    """Test encoding."""
    benchmark.group=f"encoding_{data_type}"
    benchmark(encoders[package], data)

@pytest.mark.parametrize(
    "package",
    packages,
    ids=packages,
)
@pytest.mark.parametrize(
    ("data_type", "data"),
    data.items(),
    ids=data.keys(),
)
def test_decode(benchmark, package, data_type, data):
    """Test decoding and equalness."""
    benchmark.group=f"decoding_{data_type}"
    try:
        encoded = encoders[package](data)
    except: # noqa: E722
        pytest.skip("Can't encode")
    benchmark(decoders[package], encoded)

