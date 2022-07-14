from datetime import date

from attrs import define
from attrs import evolve
from attrs import field


@define
class User:
    """User domain model."""

    last_login = field()

    @classmethod
    def new(cls):
        """Instantiate class."""
        return cls(last_login=date.today())

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30


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
class ClassMethodOnlyUser:
    """User domain model."""

    last_login = field()

    @classmethod
    def new(cls):
        """Instantiate class."""
        raise RuntimeError


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


@define
class VarArgsUser:
    """User domain model."""

    def __init__(self, *args):
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
class DoubleUnderscoreMethodUser:
    """User domain model."""

    last_login = field()

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError

    def __is_active(self):
        raise RuntimeError


@define
class UnderscoreClassMethodUser:
    """User domain model."""

    last_login = field()

    @classmethod
    def _new(cls):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@define
class DoubleUnderscoreClassMethodUser:
    """User domain model."""

    last_login = field()

    @classmethod
    def __new(cls):
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError


@define
class DunderMethodUser:
    """User domain model."""

    last_login = field()

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


@define
class DunderClassMethodUser:
    """User domain model."""

    last_login = field()

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


@define
class Bot:
    """Bot domain model."""

    last_login = field()

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


@define
class NewBot(Bot):
    """New bot domain model."""


@define
class StaticBot:
    """Bot domain model."""

    last_login = field()

    @staticmethod
    def is_bot():
        """Perform bot check."""
        raise RuntimeError

    def is_active(self):
        """Calculate user activity status."""
        raise RuntimeError
