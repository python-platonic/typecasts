import pytest

from typecasts import Typecasts


class Parent:
    """Parent class."""


class Child(Parent):
    """Derived class."""


def cast(_instance: Parent) -> str:
    """Convert."""
    return 'foo'


def test_inheritance():
    """
    We know how to convert Parent to str.

    This means we know how to convert Child to str, too.
    """
    casts = Typecasts({
        (Parent, str): cast,
    })

    assert casts[Parent, str] == cast
    assert casts[Child, str] == cast


def test_reverse_inheritance():
    """
    We know how to convert Child to str.

    But we do not know how to convert Parent to str.
    """
    casts = Typecasts({
        (Child, str): cast,
    })

    assert casts[Child, str] == cast

    with pytest.raises(KeyError):
        assert casts[Parent, str]
