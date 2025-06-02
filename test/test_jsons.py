import json

import ujson
import orjson
import msgspec
import pytest
import simplejson

encoders = {
    "json": lambda data: json.dumps(data),
    "ujson": lambda data: ujson.dumps(data),
    "orjson": lambda data: orjson.dumps(data).decode("utf-8"),
    "simplejson": lambda data: simplejson.dumps(data),
    "msgspec": lambda data: msgspec.json.encode(data).decode("utf-8"),
}

decoders = {
    "json": lambda data: json.loads(data),
    "ujson": lambda data: ujson.loads(data),
    "orjson": lambda data: orjson.loads(data.encode("utf-8")),
    "simplejson": lambda data: simplejson.loads(data),
    "msgspec": lambda data: msgspec.json.decode(data),
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
    assert data == benchmark(decode_fn, encoded)
