from abc import ABC
from abc import abstractclassmethod
from datetime import date


class UserType(ABC):
    """User interface."""

    @abstractclassmethod
    def is_active(self):
        """Calculate user activity status."""


class User(UserType):
    """User domain model."""

    def __init__(self, last_login):
        self.last_login = last_login

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30


class SmartUser:
    """User model decorator."""

    def __init__(self, user):
        self.user = user
