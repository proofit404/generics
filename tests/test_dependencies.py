"""Tests related to the compatibility with the dependencies library."""
from datetime import date

from dependencies import Injector

from generics import private


def test_instantiate(e):
    """We can instantiate private classes with injector."""

    class Container(Injector):
        user = private(e.User)
        last_login = date(1999, 12, 31)

    assert not Container.user.is_active()
