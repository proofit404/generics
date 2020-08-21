# -*- coding: utf-8 -*-
from datetime import datetime

from attr import attrs


@attrs(auto_attribs=True)
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


@attrs(auto_attribs=True)
class InheritanceUser(User):
    """Inherit user domain model."""


class PlainUser(object):
    """Plain user domain model."""


@attrs(auto_attribs=True)
class NoMethodsUser(object):
    """User domain model."""

    last_login: datetime


@attrs(auto_attribs=True)
class ClassMethodOnlyUser(object):
    """User domain model."""

    last_login: datetime

    @classmethod
    def new(cls):
        """Instantiate class."""
        pass  # pragma: no cover


@attrs(auto_attribs=True)
class NoEncapsulationUser(object):
    """User domain model."""

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


@attrs(auto_attribs=True)
class UnderscoreMethodUser(object):
    """User domain model."""

    last_login: datetime

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover

    def _is_active(self):
        pass  # pragma: no cover


supports_private_attributes = True


@attrs(auto_attribs=True)
class UnderscoreAttributeUser(object):
    """User domain model."""

    last_login: datetime
    _is_active: bool

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


@attrs(auto_attribs=True)
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


@attrs(auto_attribs=True)
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
