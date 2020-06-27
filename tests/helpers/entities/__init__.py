# -*- coding: utf-8 -*-
import pytest

import helpers


# Fixtures.


@helpers.is_not_empty
def _entities():
    try:
        import entities.dataclasses

        yield entities.dataclasses
    except (SyntaxError, ImportError):
        pass

    try:
        import entities.attrs_annotated

        yield entities.attrs_annotated
    except SyntaxError:
        pass

    import entities.attrs

    yield entities.attrs

    try:
        import entities.pydantic_model

        # The pydantic model returns str type for Optional[str] field
        # for some reason.  Probably a bug in the pydantic library.
        yield entities.pydantic_model
    except (SyntaxError, ImportError):
        pass

    try:
        import entities.pydantic_dataclasses

        yield entities.pydantic_dataclasses
    except (SyntaxError, ImportError):
        pass


@pytest.fixture(params=_entities())
def e(request):
    """Parametrized fixture with all possible entity definitions."""
    return request.param
