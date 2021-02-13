from typing import Callable, Generic, Tuple, Type, TypeVar

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
