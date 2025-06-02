import math
import json
import pprint

import ujson
import orjson
import msgspec
import pytest
import simplejson

def assert_almost_equal_with_nan(a, b, fail=None):
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
        for i, (x, y) in enumerate(zip(a, b)):
            assert_almost_equal_with_nan(x, y, fail=fail)
    elif isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            fail()
        for k in a:
            assert_almost_equal_with_nan(a[k], b[k], fail=fail)
    else:
        if a != b:
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

data = {
    "valid-floats": [1.0, 2.2, 2.5, -.43, .32, .23],
    "invalid-floats": [float("-inf"), float("inf"), float("NaN")]
}

@pytest.mark.parametrize("package, encode_fn", encoders.items())
@pytest.mark.parametrize("data_type, data", data.items())
def test_encode(benchmark, package, encode_fn, data_type, data):
    benchmark.group=f"encoding_{data_type}"
    benchmark(encode_fn, data)

@pytest.mark.parametrize("package, decode_fn", decoders.items())
@pytest.mark.parametrize("data_type, data", data.items())
def test_decode(benchmark, package, decode_fn, data_type, data):
    benchmark.group=f"decoding_{data_type}"
    encoded = encoders[package](data)
    assert_almost_equal_with_nan(data, benchmark(decode_fn, encoded))
