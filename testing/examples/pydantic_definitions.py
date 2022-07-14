from datetime import date

from pydantic.dataclasses import dataclass


@dataclass
class User:
    """User domain model."""

    last_login: date

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30
