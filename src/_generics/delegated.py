class Delegated:
    """Create decorator class in true sense of OOP."""

    def __init__(self, interface):
        self.interface = interface

    def __call__(self, cls):
        """Create decorator class."""
        created_methods = {"__init__": cls.__dict__["__init__"]}
        for name in self.interface.__dict__:
            if name.startswith("_"):
                continue
            created_methods[name] = _create_method(name)
        return type(cls.__name__, (), created_methods)


def _create_method(name):
    def _method(self, *args, **kwargs):
        return getattr(self.user, name)(*args, **kwargs)

    return _method


delegated = Delegated
