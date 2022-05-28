from datetime import datetime


class User:
    """User domain model."""

    def __init__(self, last_login):
        self.last_login = last_login

    def __repr__(self):
        return (
            self.__class__.__name__
            + "("
            + ", ".join(k + "=" + repr(v) for k, v in self.__dict__.items())
            + ")"
        )

    @classmethod
    def new(cls):
        """Instantiate class."""
        return cls(last_login=datetime.now())

    def is_active(self):
        """Calculate user activity status."""
        return (datetime.now() - self.last_login).days < 30


class InheritanceUser(User):
    """Inherit user domain model."""


class ClassMethodOnlyUser:
    """User domain model."""

    def __init__(self, last_login):
        pass  # pragma: no cover

    @classmethod
    def new(cls):
        """Instantiate class."""
        pass  # pragma: no cover


class NoMethodsUser:
    """User domain model."""

    def __init__(self, last_login):
        pass  # pragma: no cover


class NoEncapsulationUser:
    """User domain model."""

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


class UnderscoreMethodUser:
    """User domain model."""

    def __init__(self, last_login):
        pass  # pragma: no cover

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover

    def _is_active(self):
        pass  # pragma: no cover


class DoubleUnderscoreMethodUser:
    """User domain model."""

    def __init__(self, last_login):
        pass  # pragma: no cover

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover

    def __is_active(self):
        pass  # pragma: no cover


class UnderscoreClassMethodUser:
    """User domain model."""

    def __init__(self, last_login):
        pass  # pragma: no cover

    @classmethod
    def _new(cls):
        pass  # pragma: no cover

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


class DoubleUnderscoreClassMethodUser:
    """User domain model."""

    def __init__(self, last_login):
        pass  # pragma: no cover

    @classmethod
    def __new(cls):
        pass  # pragma: no cover

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


@classmethod
def _global_class_method(cls):
    return cls(last_login=datetime.now())


def _global_method(instance):
    return (datetime.now() - instance.last_login).days < 30


class GlobalMethodUser:
    """User domain model."""

    def __init__(self, last_login):
        self.last_login = last_login

    new = _global_class_method

    is_active = _global_method


class UnderscoreAttributeUser:
    """User domain model."""

    def __init__(self, last_login, _is_active):
        pass  # pragma: no cover

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover


class DunderMethodUser:
    """User domain model."""

    def __init__(self, last_login):
        self.last_login = last_login

    @classmethod
    def new(cls):
        """Instantiate class."""
        return cls(last_login=datetime.now())

    def is_active(self):
        """Calculate user activity status."""
        return (datetime.now() - self.last_login).days < 30

    def __validate__(self):
        """Validate."""
        pass  # pragma: no cover


class DunderClassMethodUser:
    """User domain model."""

    def __init__(self, last_login):
        self.last_login = last_login

    @classmethod
    def new(cls):
        """Instantiate class."""
        return cls(last_login=datetime.now())

    def is_active(self):
        """Calculate user activity status."""
        return (datetime.now() - self.last_login).days < 30

    @classmethod
    def __validate__(cls):
        """Validate."""
        pass  # pragma: no cover


class Bot:
    """Bot domain model."""

    def __init__(self, last_login):
        self.last_login = last_login

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


class StaticBot:
    """Bot domain model."""

    def __init__(self, last_login):
        pass  # pragma: no cover

    @staticmethod
    def is_bot():
        """Perform bot check."""
        pass  # pragma: no cover

    def is_active(self):
        """Calculate user activity status."""
        pass  # pragma: no cover
