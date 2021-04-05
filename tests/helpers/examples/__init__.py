import pytest


# Fixtures.


@pytest.fixture()
def e():
    """Fixture with all possible entity definitions."""
    import examples.definitions

    return examples.definitions


# FIXME: Test attrs and dataclasses compatibility the same way.


@pytest.fixture()
def p():
    """Fixture with pydantic entity definitions."""
    import examples.pydantic_definitions

    return examples.pydantic_definitions
