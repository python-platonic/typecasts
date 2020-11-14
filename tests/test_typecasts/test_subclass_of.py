from typecasts.types import SubclassOf


def test_subclass_of():
    """__origin__ attribute of the parametrized class points to parent."""
    assert SubclassOf[int].__origin__ == SubclassOf   # type: ignore
