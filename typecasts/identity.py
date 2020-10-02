from typing import TypeVar

T = TypeVar('T')  # noqa: WPS111


def identity(anything: T) -> T:
    """Identity function."""
    return anything
