import pytest

from typecasts import Typecasts, identity
from typecasts.errors import RedundantIdentity, TypecastNotFound


def test_not_found():
    """When a typecast is not found, an exception is raised."""
    with pytest.raises(TypecastNotFound) as err:
        _ = Typecasts()[str, int]  # noqa: WPS122

    expected_response = '''A method to cast one type to another was not found.

Attempted to cast

    from: <class 'str'>
    to:   <class 'int'>

Assuming you are using `typecasts.casts`,

[HINT] You may create such a function as follows:

    typecasts.casts[str, int] = ...

[HINT] Or, using decorator syntax:

@typecasts.casts.register(str, int)
def cast_str_to_int(
    source_value: str,
) -> int:
    return ...

For further details, see:

    - Examples at typecasts.defaults module
    - Or docs at https://pyplatonic.dev/typecasts/'''  # noqa: Q001

    assert str(err.value) == expected_response  # noqa: WPS441


def test_redundant_identity():
    """Adding a cast from a type to itself causes an error."""
    with pytest.raises(RedundantIdentity):
        Typecasts()[int, int] = identity
