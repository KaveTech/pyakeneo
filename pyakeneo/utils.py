import json
from collections import namedtuple
from typing import Any


def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    https://stackoverflow.com/a/11326230
    """
    return "/".join(map(lambda x: str(x).strip("/").rstrip("/"), args))


def _json_object_hook(data):
    """https://stackoverflow.com/a/15882054"""
    try:
        data["links"] = data.pop("_links")
    except KeyError as e:
        pass
    try:
        data["embedded"] = data.pop("_embedded")
    except KeyError as e:
        pass
    return namedtuple("X", data.keys(), rename=False)(*data.values())


def json2object(data):
    """https://stackoverflow.com/a/15882054"""
    return json.loads(data, object_hook=_json_object_hook)


def serialize_structured_params(params: dict[str, Any]) -> dict[str, str]:
    result = {}
    for key, value in params.items():
        if isinstance(value, str):
            result[key] = value
        else:
            result[key] = json.dumps(value)

    return result
