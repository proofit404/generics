from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    """User domain model."""

    last_login: date

    @classmethod
    def new(cls):
        """Instantiate class."""
        return cls(last_login=date.today())

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30


@dataclass
class InheritanceUser(User):
    """Inherit user domain model."""


@dataclass
class ClassMethodOnlyUser:
    """User domain model."""

    last_login: date

    @classmethod
    def new(cls):
        """Instantiate class."""
        raise RuntimeError


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
class UnderscoreMethodUser:
    """User domain model."""

    last_login: date

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError

    def _is_active(self):
        raise RuntimeError


@dataclass
class DoubleUnderscoreMethodUser:
    """User domain model."""

    last_login: date

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError

    def __is_active(self):
        raise RuntimeError


@dataclass
class UnderscoreClassMethodUser:
    """User domain model."""

    last_login: date

    @classmethod
    def _new(cls):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@dataclass
class DoubleUnderscoreClassMethodUser:
    """User domain model."""

    last_login: date

    @classmethod
    def __new(cls):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@dataclass
class UnderscoreAttributeUser:
    """User domain model."""

    last_login: date
    _is_active: bool

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@dataclass
class DunderMethodUser:
    """User domain model."""

    last_login: date

    @classmethod
    def new(cls):
        """Instantiate class."""
        return cls(last_login=date.today())

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30

    def __validate__(self):
        """Validate."""
        raise RuntimeError


@dataclass
class DunderClassMethodUser:
    """User domain model."""

    last_login: date

    @classmethod
    def new(cls):
        """Instantiate class."""
        return cls(last_login=date.today())

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30

    @classmethod
    def __validate__(cls):
        """Validate."""
        raise RuntimeError


@dataclass
class Bot:
    """Bot domain model."""

    last_login: date

    @classmethod
    def is_bot(cls):
        """Perform bot check."""
        return True

    @classmethod
    def new_bot(cls):
        """Create an instance of the `NewBot`."""
        return NewBot(last_login=date.today())

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@dataclass
class NewBot(Bot):
    """New bot domain model."""


@dataclass
class StaticBot:
    """Bot domain model."""

    last_login: date

    @staticmethod
    def is_bot():
        """Perform bot check."""
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError
