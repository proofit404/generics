"""Tests related to the compatibility with the dataclasses library."""
from datetime import date

from generics import private


def test_private_dataclass(d):
    """We can decorate dataclass with private function."""
    user_class = private(d.User)
    user = user_class(last_login=date(1999, 12, 31))
    assert not user.is_active()
