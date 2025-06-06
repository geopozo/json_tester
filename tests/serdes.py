import json

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

try:
    from custom import custom_dumps, custom_loads
    packages.append("custom")
except ImportError:
    pass

encoders = {
    "json": lambda data: json.dumps(data),
    "ujson": lambda data: ujson.dumps(data),
    "orjson": lambda data: orjson.dumps(data).decode("utf-8"),
    "simplejson": lambda data: simplejson.dumps(data, allow_nan=True),
    "msgspec": lambda data: msgspec.json.encode(data).decode("utf-8"),
    "custom": lambda data: custom_dumps(data),
}

decoders = {
    "json": lambda data: json.loads(data),
    "ujson": lambda data: ujson.loads(data),
    "orjson": lambda data: orjson.loads(data.encode("utf-8")),
    "simplejson": lambda data: simplejson.loads(data, allow_nan=True),
    "msgspec": lambda data: msgspec.json.decode(data, strict=False),
    "custom": lambda data: custom_loads(data),
}
