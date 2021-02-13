from functools import partial
from typing import Any, Callable, Dict, Iterable, Optional, Tuple, Type

from generic_args import generic_type_args

from typecasts.errors import (
    DuplicatingTypecasts,
    RedundantIdentity,
    TypecastNotFound,
)
from typecasts.identity import identity
from typecasts.types import Cast, DestinationType, Row, SourceType, SubclassOf


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

        except KeyError:
            cast_by_inheritance = self._getitem_by_inheritance(
                source_type=source_type,
                destination_type=destination_type,
            )

            if cast_by_inheritance:
                return cast_by_inheritance

            cast_parametric = self._getitem_parametric(
                source_type=source_type,
                destination_type=destination_type,
            )

            if cast_parametric:
                return cast_parametric

        raise TypecastNotFound(
            source_type=source_type,
            destination_type=destination_type,
            typecasts=self,
        )

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

    def _find_rows_by_inheritance(
        self,
        source_type: Type[SourceType],
        destination_type: Type[DestinationType],
    ) -> Iterable[Row[SourceType, DestinationType]]:
        """Find suitable conversion arrows by superclasses of SourceType."""
        for row in self.items():
            (source, destination), cast = row

            if (  # noqa: WPS337
                destination == destination_type and
                issubclass(source_type, source)
            ):
                yield row

    def _getitem_by_inheritance(
        self,
        source_type: Type[SourceType],
        destination_type: Type[DestinationType],
    ) -> Optional[Cast[SourceType, DestinationType]]:
        """
        Given A → B conversion, convert any subclass A' of A to B.

        For example, if `pydantic.BaseModel` → `JSONString` conversion is
        defined, it will also be used to convert any `CustomPydanticModel`
        to `JSONString`, where `CustomPydanticModel` is inherited from
        `pydantic.BaseModel`.

        Ground for this is Liskov Substitution Principle (LSP).

        !!! note
            This method does not work for `JSONString` → `pydantic.BaseModel`
        conversions, because for them to work the converting function must be
        aware of the target class type. Parametric typecasts solve this.
        """
        suitable_rows = list(self._find_rows_by_inheritance(
            source_type=source_type,
            destination_type=destination_type,
        ))

        if not suitable_rows:
            return None

        if len(suitable_rows) > 1:
            raise DuplicatingTypecasts(
                choices=suitable_rows,
                source_type=source_type,
                destination_type=destination_type,
                typecasts=self,
            )

        (_type_pair, cast), = suitable_rows

        return cast

    def _find_rows_parametric(   # noqa: WPS231
        self,
        source_type: Type[SourceType],
        destination_type: Type[DestinationType],
    ) -> Iterable[Row[SourceType, DestinationType]]:
        """Find suitable conversion arrows by DestinationType superclasses."""
        for row in self.items():
            (source, destination), cast = row

            if source != source_type:
                continue

            if getattr(destination, '__origin__', None) != SubclassOf:
                continue

            destination_superclass, = generic_type_args(destination)

            if not issubclass(destination_type, destination_superclass):
                continue  # pragma: no cover

            yield row

    def _getitem_parametric(
        self,
        source_type: Type[SourceType],
        destination_type: Type[DestinationType],
    ) -> Optional[Cast[SourceType, DestinationType]]:
        """
        Given A → SubclassOf[B], convert instance of A to requested B subclass.

        For example, if `JSONString` → `SubclassOf[pydantic.BaseModel]`
        conversion is defined, it will be a function with signature

            def convert(value: JSONString, destination_type: Type[T]) -> T:

        where `T` is bound by `pydantic.BaseModel`.

        This function will return

            partial(
                convert,
                destination_type=CustomPydanticModel,
            )

        to preserve the correct signature of a normal conversion function.
        """
        suitable_rows = list(self._find_rows_parametric(
            source_type=source_type,
            destination_type=destination_type,
        ))

        if not suitable_rows:
            return None

        if len(suitable_rows) > 1:  # pragma: no cover
            raise DuplicatingTypecasts(
                choices=suitable_rows,
                source_type=source_type,
                destination_type=destination_type,
                typecasts=self,
            )

        (_type_pair, cast), = suitable_rows

        return partial(
            cast,
            destination_type=destination_type,
        )
