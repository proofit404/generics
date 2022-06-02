"""Tests related to the @delegated decorator."""
from datetime import datetime

from generics import delegated
from generics import private


def test_define_instance_methods(e, w):
    """Provide access to not redefined methods."""
    user_class = private(e.User)
    smart_user_class = delegated(user_class)(w.SmartUser)
    user = user_class(last_login=datetime(1999, 12, 31))
    smart_user = smart_user_class(user)
    assert not smart_user.is_active()
