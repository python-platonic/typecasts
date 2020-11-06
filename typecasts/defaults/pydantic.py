from typing import Type, TypeVar

import pydantic

from typecasts.defaults.base import casts


PydanticModel = TypeVar('PydanticModel', bound=pydantic.BaseModel)


@casts.register(pydantic.BaseModel, str)
def pydantic_to_json_string(instance: pydantic.BaseModel) -> str:
    """Convert Pydantic model instance to JSON string."""
    return instance.json()
