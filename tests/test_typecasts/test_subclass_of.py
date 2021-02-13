from typecasts.types import SubclassOf


def test_subclass_of():
    """__origin__ attribute of the parametrized class points to parent."""
    origin = SubclassOf[int].__origin__  # type: ignore   # noqa: WPS609
    assert origin == SubclassOf
