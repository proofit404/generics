"""Tests related to the compatibility with the attrs library."""
from datetime import date

from generics import private


def test_private_attrs(a):
    """We can decorate attrs class with private function."""
    user_class = private(a.User)
    user = user_class(last_login=date(1999, 12, 31))
    assert not user.is_active()
