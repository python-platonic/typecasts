import pytest

from typecasts import Typecasts, identity
from typecasts.errors import RedundantIdentity, TypecastNotFound


class MyType:
    """My little brave class."""


def test_identity():
    """Request to cast from a type to itself is an identity function."""
    assert Typecasts()[float, float] == identity
    assert Typecasts()[MyType, MyType] == identity


def test_not_found():
    """When a typecast is not found, an exception is raised."""
    with pytest.raises(TypecastNotFound):
        _ = Typecasts()[str, int]  # noqa: WPS122


def test_set_item():
    """Set and get a typecast."""
    typecasts = Typecasts()
    typecasts[int, str] = str
    assert typecasts[int, str] == str


def test_redundant_identity():
    """Adding a cast from a type to itself causes an error."""
    with pytest.raises(RedundantIdentity):
        Typecasts()[int, int] = identity
