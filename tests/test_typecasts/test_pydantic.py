import pydantic
import pytest

from typecasts import casts


class Wizard(pydantic.BaseModel):
    """Wizard definition."""

    name: str


def test_from_pydantic_to_str():
    """Convert pydantic model to JSON string."""
    converter = casts[Wizard, str]

    assert converter(Wizard(name='Rincewind')) == '{"name": "Rincewind"}'


@pytest.mark.skip('Parametric transformations not implemented yet.')
def test_from_str_to_pydantic():
    """Parse JSON string to pydantic model."""
    parser = casts[str, Wizard]
    assert parser('{"name": "Rincewind"}') == Wizard(name='Rincewind')
