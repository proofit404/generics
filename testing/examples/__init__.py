import pytest


# Fixtures.


@pytest.fixture()
def e():
    """Fixture with all possible entity definitions."""
    import examples.definitions

    return examples.definitions


@pytest.fixture()
def s():
    """Fixture with subtyping entity definitions."""
    import examples.sybtyping_definitions

    return examples.sybtyping_definitions


@pytest.fixture()
def a():
    """Fixture with attrs entity definitions."""
    import examples.attrs_definitions

    return examples.attrs_definitions


@pytest.fixture()
def d():
    """Fixture with dataclass entity definitions."""
    import examples.dataclass_definitions

    return examples.dataclass_definitions


@pytest.fixture()
def p():
    """Fixture with pydantic entity definitions."""
    import examples.pydantic_definitions

    return examples.pydantic_definitions
