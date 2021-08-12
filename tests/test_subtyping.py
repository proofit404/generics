"""Tests related to inheritance from interface."""
from datetime import datetime

import pytest

from generics import defended
from generics import delegated
from generics import private


pytestmark = pytest.mark.parametrize("f", [private, delegated, defended])


def test_allow_inheritance_from_interface(f, s):
    """Allow inheritance from interface."""
    user_class = f(s.User)
    user = user_class(last_login=datetime(1999, 12, 31))
    assert not user.is_active()
