class Delegated:
    """Create decorator class in true sense of OOP."""

    def __init__(self, interface):
        self.interface = interface

    def __call__(self, cls):
        """Create decorator class."""
        created_methods = {
            name: _create_method(name)
            for name in self.interface.__dict__
            if not name.startswith("_")
        }
        created_methods["__init__"] = cls.__dict__["__init__"]
        return type(cls.__name__, (), created_methods)


def _create_method(name):
    def _method(self, *args, **kwargs):
        return getattr(self.user, name)(*args, **kwargs)

    return _method


delegated = Delegated
