from typecasts import Typecasts

typecasts = Typecasts()


@typecasts.register(bool, str)
def bool_to_str(boolean: bool) -> str:
    """Bool to str."""
    return str(boolean)


def test_register():
    """Confirm that @register works correctly."""
    assert typecasts[bool, str](True) == 'True'
