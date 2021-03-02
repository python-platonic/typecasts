from dataclasses import dataclass

from typecasts import casts
from typecasts.types import Dataclass, JSONString


@dataclass
class Cat:
    """Cat."""

    name: str


def test_is_subclass():
    """Check issubclass() performance."""
    assert issubclass(Cat, Dataclass)
    assert not issubclass(int, Dataclass)
    assert not issubclass(object, Dataclass)


def test_is_instance():
    """Check isinstance() performance."""
    assert not isinstance(Cat, Dataclass)
    assert not isinstance(5, Dataclass)
    assert not isinstance(object, Dataclass)
    assert isinstance(Cat(name='Ray'), Dataclass)


def test_json_serialization():
    """Serialize to JSON and deserialize back."""
    cat = Cat(name='Furry')

    serialized = JSONString('{"name": "Furry"}')
    assert casts[Cat, JSONString](cat) == serialized
    assert casts[JSONString, Cat](serialized) == cat
