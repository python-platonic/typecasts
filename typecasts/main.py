from typing import Any, Callable, Dict, Tuple, Type, TypeVar

from typecasts.errors import RedundantIdentity, TypecastNotFound
from typecasts.identity import identity

SourceType = TypeVar('SourceType')
DestinationType = TypeVar('DestinationType')

TypePair = Tuple[Type[SourceType], Type[DestinationType]]
Cast = Callable[[SourceType], DestinationType]


# Regrettably, we *have* to use `Any` here. I do not see any other way.
class Typecasts(Dict[  # type: ignore
    Tuple[type, type],
    Callable[[Any], Any],
]):
    """Typecasts repository."""

    def __getitem__(
        self,
        type_pair: Tuple[Type[SourceType], Type[DestinationType]],
    ) -> Callable[[SourceType], DestinationType]:
        """Get typecast function for given type pair."""
        source_type, destination_type = type_pair

        if source_type == destination_type:
            return identity  # type: ignore

        try:
            return super().__getitem__(type_pair)

        except KeyError as err:
            # FIXME This seems to violate Liskov substitution principle.
            #   Shall we remove the inheritance from Dict?
            raise TypecastNotFound(
                source_type=source_type,
                destination_type=destination_type,
                typecasts=self,
            ) from err

    def __setitem__(
        self,
        type_pair: Tuple[Type[SourceType], Type[DestinationType]],
        cast: Callable[[SourceType], DestinationType],
    ) -> None:
        """Specify typecast function for given type pair."""
        source_type, destination_type = type_pair

        if source_type == destination_type:
            raise RedundantIdentity(
                idempotent_type=source_type,
                typecasts=self,
            )

        return super().__setitem__(type_pair, cast)

    def register(
        self,
        source_type: Type[SourceType],
        destination_type: Type[DestinationType],
    ):
        """Decorator to register a function as a typecast."""
        def registrar(  # noqa: WPS430
            function: Callable[[SourceType], DestinationType],
        ):
            self[source_type, destination_type] = function
            return function

        return registrar
