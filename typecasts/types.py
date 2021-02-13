from typing import Callable, Tuple, Type, TypeVar, Generic

SourceType = TypeVar('SourceType')
DestinationType = TypeVar('DestinationType')

TypePair = Tuple[Type[SourceType], Type[DestinationType]]

Cast = Callable[[SourceType], DestinationType]

Row = Tuple[
    TypePair[SourceType, DestinationType],
    Cast[SourceType, DestinationType],
]

T = TypeVar('T')


class SubclassOf(Generic[T]):
    """Represent a subclass of a certain type for parametric conversion."""
