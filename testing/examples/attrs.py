from datetime import date

from attr import attrib
from attr import attrs
from attr import evolve


@attrs
class User:
    """User domain model."""

    last_login = attrib()

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30


@attrs
class StaticMethodUser:
    """User domain model."""

    last_login = attrib()

    @staticmethod
    def is_bot():
        """Perform bot check."""
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@attrs
class ClassMethodUser:
    """User domain model."""

    last_login = attrib()

    @classmethod
    def new(cls):
        """Instantiate class."""
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@attrs
class NamedUser:
    """User domain model."""

    name = attrib()

    def greet(self):
        """Say nice thing."""
        return f"Hello, {self.name}"

    def rename(self, name):
        """Change user name."""
        return evolve(self, name=name)


@attrs
class InheritanceUser(User):
    """Inherit user domain model."""


@attrs
class NoMethodsUser:
    """User domain model."""

    last_login = attrib()


@attrs
class NoEncapsulationUser:
    """User domain model."""

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@attrs(init=False)
class VarArgsUser:
    """User domain model."""

    def __init__(self, *args):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@attrs(init=False)
class KwArgsUser:
    """User domain model."""

    def __init__(self, **kwargs):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@attrs
class UnderscoreMethodUser:
    """User domain model."""

    last_login = attrib()

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError

    def _is_active(self):
        raise RuntimeError


@attrs
class ClassAttributeUser:
    """User domain model."""

    has_profile = True

    last_login = attrib()

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError
