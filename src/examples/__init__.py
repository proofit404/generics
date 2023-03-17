import pytest


# Fixtures.


def _definitions():
    import examples.definitions
    import examples.attrs
    import examples.attrs_define
    import examples.dataclasses
    import examples.pydantic

    yield examples.definitions
    yield examples.attrs
    yield examples.attrs_define
    yield examples.dataclasses
    yield examples.pydantic


@pytest.fixture(
    params=_definitions(),
    ids=["definitions", "attrs", "attrs_define", "dataclass", "pydantic"],
)
def e(request):
    """Fixture with all possible entity definitions."""
    return request.param
