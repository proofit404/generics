from datetime import date

from attrs import define
from attrs import evolve
from attrs import field


@define
class User:
    """User domain model."""

    last_login = field()

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30


@define
class StaticMethodUser:
    """User domain model."""

    last_login = field()

    @staticmethod
    def is_bot():
        """Perform bot check."""
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@define
class ClassMethodUser:
    """User domain model."""

    last_login = field()

    @classmethod
    def new(cls):
        """Instantiate class."""
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@define
class NamedUser:
    """User domain model."""

    name = field()

    def greet(self):
        """Say nice thing."""
        return f"Hello, {self.name}"

    def rename(self, name):
        """Change user name."""
        return evolve(self, name=name)


@define
class InheritanceUser(User):
    """Inherit user domain model."""


@define
class NoMethodsUser:
    """User domain model."""

    last_login = field()


@define
class NoEncapsulationUser:
    """User domain model."""

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@define(init=False)
class VarArgsUser:
    """User domain model."""

    def __init__(self, *args):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@define(init=False)
class KwArgsUser:
    """User domain model."""

    def __init__(self, **kwargs):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@define
class UnderscoreMethodUser:
    """User domain model."""

    last_login = field()

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError

    def _is_active(self):
        raise RuntimeError


@define
class ClassAttributeUser:
    """User domain model."""

    has_profile = True

    last_login = field()

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError
