from typecasts.defaults.base import casts

# Configure pydantic rules if Pydantic is installed.
try:
    from typecasts.defaults import pydantic
except ImportError:   # pragma: no cover
    ...


from typecasts.defaults import dataclass
