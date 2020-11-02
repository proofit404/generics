import pytest

import helpers


# Fixtures.


@helpers.is_not_empty
def _examples():
    import examples.attrs
    import examples.attrs_annotated
    import examples.dataclasses
    import examples.pydantic_dataclasses
    import examples.pydantic_model

    yield examples.attrs
    yield examples.attrs_annotated
    yield examples.dataclasses
    yield examples.pydantic_dataclasses
    yield examples.pydantic_model


@pytest.fixture(params=_examples())
def e(request):
    """Parametrized fixture with all possible entity definitions."""
    return request.param
