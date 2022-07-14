import pytest


# Fixtures.


def _definitions():
    import examples.definitions
    import examples.attrs
    import examples.dataclasses
    import examples.pydantic

    yield examples.definitions
    yield examples.attrs
    yield examples.dataclasses
    yield examples.pydantic


@pytest.fixture(
    params=_definitions(),
    ids=["definitions", "attrs", "dataclass", "pydantic"],
)
def e(request):
    """Fixture with all possible entity definitions."""
    return request.param


@pytest.fixture()
def w():
    """Fixture with all possible entity decorators."""
    import examples.delegates

    return examples.delegates


@pytest.fixture()
def s():
    """Fixture with subtyping entity definitions."""
    import examples.subtyping

    return examples.subtyping
