from typing import Callable, Tuple, Type, TypeVar

SourceType = TypeVar('SourceType')
DestinationType = TypeVar('DestinationType')

TypePair = Tuple[Type[SourceType], Type[DestinationType]]

Cast = Callable[[SourceType], DestinationType]

Row = Tuple[
    TypePair[SourceType, DestinationType],
    Cast[SourceType, DestinationType],
]
