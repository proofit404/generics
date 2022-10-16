from generics import delegate
from generics import private


@private
class SmartUser:
    """User model decorator."""

    def __init__(self, user):
        self.user = user
        self.called = False

    def was_called(self):
        """Check called delegate status."""
        return self.called

    @delegate
    def smart(self, name, args, kwargs):
        """Handle methods dynamically."""
        self.called = True
        method = getattr(self.user, name)
        return method(*args, **kwargs)
