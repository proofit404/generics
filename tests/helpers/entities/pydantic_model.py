from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    """User domain model."""

    last_login: datetime

    @classmethod
    def new(cls):
        """Instantiate class."""
        return cls(last_login=datetime.now())

    def is_active(self):
        """Calculate user activity status."""
        return (datetime.now() - self.last_login).days < 30


class InheritanceUser(User):
    """Inherit user domain model."""


class PlainUser:
    """Plain user domain model."""


class NoMethodsUser(BaseModel):
    """User domain model."""

    last_login: datetime


class ClassMethodOnlyUser(BaseModel):
    """User domain model."""

    last_login: datetime

    @classmethod
    def new(cls):
        """Instantiate class."""
        pass  # pragma: no cover


class NoEncapsulationUser(BaseModel):
    """User domain model."""

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


class UnderscoreMethodUser(BaseModel):
    """User domain model."""

    last_login: datetime

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover

    def _is_active(self):
        pass  # pragma: no cover


supports_private_attributes = False


class Bot(BaseModel):
    """Bot domain model."""

    last_login: datetime

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


class StaticBot(BaseModel):
    """Bot domain model."""

    last_login: datetime

    @staticmethod
    def is_bot():
        """Perform bot check."""
        pass  # pragma: no cover

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


supports_dependencies = False
