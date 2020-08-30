from datetime import datetime

from attr import attrib
from attr import attrs


@attrs
class User:
    """User domain model."""

    last_login = attrib()

    @classmethod
    def new(cls):
        """Instantiate class."""
        return cls(last_login=datetime.now())

    def is_active(self):
        """Calculate user activity status."""
        return (datetime.now() - self.last_login).days < 30


@attrs
class InheritanceUser(User):
    """Inherit user domain model."""


class PlainUser:
    """Plain user domain model."""


@attrs
class ClassMethodOnlyUser:
    """User domain model."""

    last_login = attrib()

    @classmethod
    def new(cls):
        """Instantiate class."""
        pass  # pragma: no cover


@attrs
class NoMethodsUser:
    """User domain model."""

    last_login = attrib()


@attrs
class NoEncapsulationUser:
    """User domain model."""

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


@attrs
class UnderscoreMethodUser:
    """User domain model."""

    last_login = attrib()

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover

    def _is_active(self):
        pass  # pragma: no cover


supports_private_attributes = True


@attrs
class UnderscoreAttributeUser:
    """User domain model."""

    last_login = attrib()
    _is_active = attrib()

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


@attrs
class Bot:
    """Bot domain model."""

    last_login = attrib()

    @classmethod
    def is_bot(cls):
        """Perform bot check."""
        return True

    @classmethod
    def new_bot(cls):
        """Create an instance of the `NewBot`."""
        return NewBot(last_login=datetime.now())

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


class NewBot(Bot):
    """New bot domain model."""


@attrs
class StaticBot:
    """Bot domain model."""

    last_login = attrib()

    @staticmethod
    def is_bot():
        """Perform bot check."""
        pass  # pragma: no cover

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


supports_dependencies = True
