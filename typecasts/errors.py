import typing
from dataclasses import dataclass

from documented import DocumentedError

if typing.TYPE_CHECKING:  # pragma: nocover
    # This one is always available in dev environment, we let mypy to use it.
    from backports.cached_property import cached_property

else:
    # In production environment, we will choose the library that is available.
    try:
        from functools import cached_property

    except ImportError:  # pragma: nocover
        # For Python <3.8
        from backports.cached_property import cached_property


if typing.TYPE_CHECKING:  # pragma: no cover
    # This is to avoid circular imports in the form of
    #     typecasts.errors ⇆ typecasts.main
    from typecasts import Typecasts


@dataclass
class RedundantIdentity(DocumentedError):
    """
    Attempted to register redundant identity function.

    At {self.typecasts}, it has been attempted to register a cast function to
    convert {self.idempotent_type} to itself, which does not make sense.

    `typecasts` will automatically use an identity function for such
    conversions.

    """

    typecasts: 'Typecasts'
    idempotent_type: type


@dataclass
class TypecastNotFound(DocumentedError):
    """
    A method to cast one type to another was not found.

    Attempted to cast

        from: {self.source_type}
        to:   {self.destination_type}

    Assuming you are using `typecasts.casts`,

    [HINT] You may create such a function as follows:

        typecasts.casts[{self.source_name}, {self.destination_name}] = ...

    [HINT] Or, using decorator syntax:

    @typecasts.casts.register({self.source_name}, {self.destination_name})
    def cast_{self.source_name_lower}_to_{self.destination_name_lower}(
        source_value: {self.source_name},
    ) -> {self.destination_name}:
        return ...

    For further details, see:

        - Examples at typecasts.defaults module
        - Or docs at https://pyplatonic.dev/typecasts/
    """

    source_type: type
    destination_type: type
    typecasts: 'Typecasts'

    @cached_property
    def source_name(self):
        """Source type name."""
        return self.source_type.__name__

    @cached_property
    def destination_name(self):
        """Destination type name."""
        return self.destination_type.__name__

    @property
    def source_name_lower(self):
        """Lowercase version of source type name."""
        return self.source_name.lower()

    @property
    def destination_name_lower(self):
        """Lowercase version of destination type name."""
        return self.destination_name.lower()
