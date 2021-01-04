import pytest


# Fixtures.


@pytest.fixture()
def e():
    """Fixture with all possible entity definitions."""
    import examples.definitions

    return examples.definitions
