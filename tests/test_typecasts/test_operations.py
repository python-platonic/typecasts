from typecasts import Typecasts, identity


class MyType:
    """My little brave class."""


def test_identity():
    """Request to cast from a type to itself is an identity function."""
    assert Typecasts()[float, float] == identity
    assert Typecasts()[MyType, MyType] == identity


def test_set_item():
    """Set and get a typecast."""
    typecasts = Typecasts()
    typecasts[int, str] = str
    assert typecasts[int, str] == str
