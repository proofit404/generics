from dataclasses import replace
from datetime import date

from pydantic.dataclasses import dataclass


@dataclass
class User:
    """User domain model."""

    last_login: date

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30


@dataclass
class StaticMethodUser:
    """User domain model."""

    last_login: date

    @staticmethod
    def is_bot():
        """Perform bot check."""
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@dataclass
class ClassMethodUser:
    """User domain model."""

    last_login: date

    @classmethod
    def new(cls):
        """Instantiate class."""
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@dataclass
class NamedUser:
    """User domain model."""

    name: str

    def greet(self):
        """Say nice thing."""
        return f"Hello, {self.name}"

    def rename(self, name):
        """Change user name."""
        return replace(self, name=name)


@dataclass
class InheritanceUser(User):
    """Inherit user domain model."""


@dataclass
class NoMethodsUser:
    """User domain model."""

    last_login: date


@dataclass
class NoEncapsulationUser:
    """User domain model."""

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@dataclass
class VarArgsUser:
    """User domain model."""

    def __init__(self, *args):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@dataclass
class KwArgsUser:
    """User domain model."""

    def __init__(self, **kwargs):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@dataclass
class UnderscoreMethodUser:
    """User domain model."""

    last_login: date

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError

    def _is_active(self):
        raise RuntimeError


@dataclass
class ClassAttributeUser:
    """User domain model."""

    has_profile = True

    last_login: date

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError
