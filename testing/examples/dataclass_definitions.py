from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    """User domain model."""

    last_login: date

    def is_active(self):
        """Calculate user activity status."""
        return (date.today() - self.last_login).days < 30
