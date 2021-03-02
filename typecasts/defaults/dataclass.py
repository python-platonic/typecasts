import dataclasses
import json
from typing import Type

from typecasts.defaults.base import casts
from typecasts.types import Dataclass, JSONString, SubclassOf


@casts.register(Dataclass, JSONString)
def dataclass_to_json_string(dataclass_value: Dataclass) -> JSONString:
    """Serialize dataclass to JSON."""
    return JSONString(json.dumps(dataclasses.asdict(dataclass_value)))


@casts.register(JSONString, SubclassOf[Dataclass])
def json_string_to_dataclass(
    serialized_value: JSONString,
    destination_type: Type[Dataclass],
) -> Dataclass:
    """Convert JSON string to specified dataclass type."""
    return destination_type(  # type: ignore
        **json.loads(serialized_value),
    )
