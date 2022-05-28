from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    """User domain model."""

    last_login: datetime

    def is_active(self):
        """Calculate user activity status."""
        return (datetime.now() - self.last_login).days < 30
