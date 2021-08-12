from abc import ABC
from abc import abstractclassmethod
from datetime import datetime


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
        return (datetime.now() - self.last_login).days < 30
