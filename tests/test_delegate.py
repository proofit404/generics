"""Tests related to the @delegated decorator."""
from datetime import date

from generics import private


def test_define_instance_methods(e, w):
    """Provide access to not redefined methods."""
    user_class = private(e.User)
    user = user_class(last_login=date(1999, 12, 31))
    smart_user = w.SmartUser(user)
    assert not smart_user.is_active()
    assert smart_user.was_called()
