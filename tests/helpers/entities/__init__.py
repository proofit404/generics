import pytest

import helpers


# Fixtures.


@helpers.is_not_empty
def _entities():
    import entities.attrs
    import entities.attrs_annotated
    import entities.dataclasses
    import entities.pydantic_dataclasses
    import entities.pydantic_model

    yield entities.attrs
    yield entities.attrs_annotated
    yield entities.dataclasses
    yield entities.pydantic_dataclasses
    yield entities.pydantic_model


@pytest.fixture(params=_entities())
def e(request):
    """Parametrized fixture with all possible entity definitions."""
    return request.param
