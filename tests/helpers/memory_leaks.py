import pympler.muppy
import pytest


# Fixtures.


@pytest.fixture(autouse=True)
def _has_memory_leaks():
    """Assert all objects was destroyed after tests."""
    all_objects = pympler.muppy.get_objects()
    yield
    assert len(all_objects) == len(pympler.muppy.get_objects())
