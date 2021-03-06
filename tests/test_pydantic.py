"""Tests related to the compatibility with the pydantic library."""
from datetime import datetime

from generics import private


def test_private_dataclass(p):
    """We can decorate pydantic dataclass with private function."""
    user_class = private(p.User)
    user = user_class(last_login=datetime(1999, 12, 31))
    assert not user.is_active()
