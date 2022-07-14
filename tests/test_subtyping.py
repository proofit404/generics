"""Tests related to inheritance from interface."""
from datetime import date

from generics import delegated
from generics import private


def test_private_allow_inheritance_from_interface(s):
    """Allow inheritance from interface."""
    user_class = private(s.User)
    user = user_class(last_login=date(1999, 12, 31))
    assert not user.is_active()


def test_delegated_allow_inheritance_from_interface(s):
    """Allow inheritance from interface."""
    user_class = private(s.User)
    smart_user_class = delegated(s.UserType)(s.SmartUser)
    user = user_class(last_login=date(1999, 12, 31))
    smart_user = smart_user_class(user)
    assert not smart_user.is_active()
