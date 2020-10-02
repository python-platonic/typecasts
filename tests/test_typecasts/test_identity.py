from typecasts import identity


def test_identity():
    """Identity is identity."""
    assert identity(5) == 5
    assert identity('foo') == 'foo'
