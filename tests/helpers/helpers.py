import functools


def is_not_empty(f):
    """Assert generator yields value at least once."""

    @functools.wraps(f)
    def wrapper():
        count = 0
        for value in f():
            count += 1
            yield value
        assert count > 0

    return wrapper
