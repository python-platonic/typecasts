from typing_extensions import TypedDict

from typecasts import casts


class Wizard(TypedDict):
    """Wizard definition."""

    name: str


def test_typed_dict_to_str():
    """Convert a TypedDict-based dict into JSON str."""
    converter = casts[Wizard, str]
    assert converter(Wizard(name='Rincewind')) == '{"name": "Rincewind"}'
