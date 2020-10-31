import pydantic

from typecasts import casts


class Wizard(pydantic.BaseModel):
    """Wizard definition."""

    name: str


def test_from_pydantic_to_str():
    """Convert pydantic model to JSON string."""
    converter = casts[Wizard, str]

    assert converter(Wizard(name='Rincewind')) == '{"name": "Rincewind"}'
