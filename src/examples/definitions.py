from datetime import date


class User:
    """User domain model."""

    def __init__(self, last_login):
        self.last_login = last_login

    def __repr__(self):
        return f"User({self.last_login=!r})"

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30


class StaticMethodUser:
    """User domain model."""

    def __init__(self, last_login):
        raise RuntimeError

    @staticmethod
    def is_bot():
        """Perform bot check."""
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


class ClassMethodUser:
    """User domain model."""

    def __init__(self, last_login):
        raise RuntimeError

    @classmethod
    def new(cls):
        """Instantiate class."""
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


class NamedUser:
    """User domain model."""

    def __init__(self, name):
        self.name = name

    def greet(self):
        """Say nice thing."""
        return f"Hello, {self.name}"

    def rename(self, name):
        """Change user name."""
        return self.__class__(name)


class InheritanceUser(User):
    """Inherit user domain model."""


class NoMethodsUser:
    """User domain model."""

    def __init__(self, last_login):
        raise RuntimeError


class NoEncapsulationUser:
    """User domain model."""

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


class VarArgsUser:
    """User domain model."""

    def __init__(self, *args):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


class KwArgsUser:
    """User domain model."""

    def __init__(self, **kwargs):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


class UnderscoreMethodUser:
    """User domain model."""

    def __init__(self, last_login):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError

    def _is_active(self):
        raise RuntimeError


class UnderscoreAttributeUser:
    """User domain model."""

    def __init__(self, last_login, _is_active):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


class ClassAttributeUser:
    """User domain model."""

    has_profile = True

    def __init__(self, last_login):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError
