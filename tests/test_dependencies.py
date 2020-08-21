# -*- coding: utf-8 -*-
"""Tests related to the compatibility with the dependencies library."""
from datetime import datetime

from dependencies import Injector

from generics import private


def test_instantiate(e):
    """We can instantiate private classes with injector."""
    if e.supports_dependencies:

        class Container(Injector):
            user = private(e.User)
            last_login = datetime(1999, 12, 31)

        assert not Container.user.is_active()
