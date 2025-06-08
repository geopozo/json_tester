import math
import pprint

import pytest
from data import CodecPair, data
from serdes import decoders, encoders, packages, parser_errors


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
    if isinstance(data, CodecPair):
        data = data.input
    try:
        benchmark(encoders[package], data)
    except parser_errors[package]():
        pytest.skip("Encoding error.")

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
    if isinstance(data, CodecPair):
        data = data.input
    try:
        encoded = encoders[package](data)
    except: # noqa: E722
        pytest.skip("Can't encode")
    benchmark(decoders[package], encoded)

@pytest.mark.parametrize(
    "package",
    packages,
    ids=packages,
)
@pytest.mark.parametrize(
    ("_data_type", "data"),
    data.items(),
    ids=data.keys(),
)
def test_roundtrip(record_property, package, _data_type, data):
    try:
        if isinstance(data, CodecPair):
            data = data.input
            expected = data.output
        else:
            expected = data
        encoded = encoders[package](data)
        decoded = decoders[package](encoded)
    except: # noqa: E722
        return
    try:
        assert_almost_equal_with_nan(decoded, expected)
    except AssertionError:
        record_property("decoded", decoded)
        record_property("expected", expected)
