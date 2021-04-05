from datetime import datetime

from pydantic.dataclasses import dataclass


@dataclass
class User:
    """User domain model."""

    last_login: datetime

    def is_active(self):
        """Calculate user activity status."""
        return (datetime.now() - self.last_login).days < 30
