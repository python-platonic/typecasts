"""This is a very strange example."""
import re

import pytest

from typecasts import Typecasts
from typecasts.errors import DuplicatingTypecasts


class Female:
    """One parent class."""


class Male:
    """Another parent class."""


class Hermaphrodite(Female, Male):
    """Derived class."""


genders = Typecasts()


@genders.register(Female, str)
def female_to_string(_female: Female) -> str:
    """Serialize a Female to a string."""
    return 'She/her'


@genders.register(Male, str)
def male_to_string(_male: Male) -> str:
    """Serialize a Male to a string."""
    return 'He/his'


ERROR_TEXT = '''Multiple methods to cast one type to another were found.

Attempted to cast:

    from: <class 'test_typecasts.test_multiple_inheritance.Hermaphrodite'>
    to:   <class 'str'>

Available choices:

    <class 'test_typecasts.test_multiple_inheritance.Female'> → <class 'str'> \
via <function female_to_string at *>
    <class 'test_typecasts.test_multiple_inheritance.Male'> → <class 'str'> \
via <function male_to_string at *>

System cannot choose between them because no priority mechanism is currently
implemented.

!!! note
    To quickly resolve this, you can create your own cast for the particular
    type in question.
'''


def test_multiple_inheritance():
    """
    We know how to convert Female to string and Male to string.

    But, Hermaphrodite is derived from both of them. It is impossible
    to determine which conversion to use, and we throw an error.
    """
    with pytest.raises(DuplicatingTypecasts) as err:
        assert genders[Hermaphrodite, str]

    error_text = str(err.value)  # noqa: WPS441

    # Replace the dynamic parts of the exception text.
    error_text = re.sub(
        r' at [^>]+',
        ' at *',
        error_text,
    )

    assert error_text == ERROR_TEXT.strip()
