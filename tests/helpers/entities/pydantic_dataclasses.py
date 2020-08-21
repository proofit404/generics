# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic.dataclasses import dataclass


@dataclass
class User:
    """User domain model."""

    last_login: datetime

    @classmethod
    def new(cls):
        """Instantiate class."""
        return cls(last_login=datetime.now())

    def is_active(self):
        """Calculate user activity status."""
        return (datetime.now() - self.last_login).days < 30


@dataclass
class InheritanceUser(User):
    """Inherit user domain model."""


class PlainUser(object):
    """Plain user domain model."""


@dataclass
class NoMethodsUser(object):
    """User domain model."""

    last_login: datetime


@dataclass
class ClassMethodOnlyUser(object):
    """User domain model."""

    last_login: datetime

    @classmethod
    def new(cls):
        """Instantiate class."""
        pass  # pragma: no cover


@dataclass
class NoEncapsulationUser(object):
    """User domain model."""

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


@dataclass
class UnderscoreMethodUser(object):
    """User domain model."""

    last_login: datetime

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover

    def _is_active(self):
        pass  # pragma: no cover


supports_private_attributes = True


@dataclass
class UnderscoreAttributeUser(object):
    """User domain model."""

    last_login: datetime
    _is_active: bool

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


@dataclass
class Bot(object):
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


@dataclass
class StaticBot(object):
    """Bot domain model."""

    last_login: datetime

    @staticmethod
    def is_bot():
        """Perform bot check."""
        pass  # pragma: no cover

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


supports_dependencies = True
