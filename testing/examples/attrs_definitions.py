from datetime import datetime

from attr import attrib
from attr import attrs


@attrs
class User:
    """User domain model."""

    last_login = attrib()

    def is_active(self):
        """Calculate user activity status."""
        return (datetime.now() - self.last_login).days < 30
