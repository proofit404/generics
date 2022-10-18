class Delegate:
    """Create decorator class in true sense of OOP."""

    def __init__(self, f):
        self.f = f


delegate = Delegate


def _dynamic(f):
    def _getattr(instance, name):
        def _bound_method(*args, **kwargs):
            return f(instance, name, args, kwargs)

        return _bound_method

    return _getattr
