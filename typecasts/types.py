import abc
import dataclasses
from typing import Callable, Generic, Tuple, Type, TypeVar, NewType

SourceType = TypeVar('SourceType')
DestinationType = TypeVar('DestinationType')

TypePair = Tuple[Type[SourceType], Type[DestinationType]]

Cast = Callable[[SourceType], DestinationType]

Row = Tuple[
    TypePair[SourceType, DestinationType],
    Cast[SourceType, DestinationType],
]

T = TypeVar('T')  # noqa: WPS111


class SubclassOf(Generic[T]):
    """Represent a subclass of a certain type for parametric conversion."""


class Dataclass(metaclass=abc.ABCMeta):
    """Type of all dataclasses."""

    @classmethod
    def __subclasshook__(cls, other_class) -> bool:
        """Determine if certain class is a dataclass."""
        return (
            isinstance(other_class, type) and
            dataclasses.is_dataclass(other_class)
        )


# Type for strings which contain valid JSON data.
JSONString = NewType('JSONString', str)
