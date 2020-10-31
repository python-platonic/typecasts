import pydantic

from typecasts.defaults.base import casts


@casts.register(pydantic.BaseModel, str)
def pydantic_to_json_string(instance: pydantic.BaseModel) -> str:
    """Convert Pydantic model instance to JSON string."""
    return instance.json()
