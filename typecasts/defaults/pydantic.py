from typing import Type, TypeVar

import pydantic

from typecasts.defaults.base import casts
from typecasts.types import SubclassOf

PydanticModel = TypeVar('PydanticModel', bound=pydantic.BaseModel)


@casts.register(pydantic.BaseModel, str)
def pydantic_to_json_string(instance: pydantic.BaseModel) -> str:
    """Convert Pydantic model instance to JSON string."""
    return instance.json()


@casts.register(str, SubclassOf[pydantic.BaseModel])
def json_string_to_pydantic(
    serialized_value: str,
    destination_type: Type[PydanticModel],
) -> PydanticModel:
    """Convert a JSON representation of a Pydantic model into model instance."""
    return pydantic.parse_raw_as(destination_type, serialized_value)
