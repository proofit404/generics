class GenericError(Exception):
    """Base error of all generics errors."""

    pass


class GenericClassError(GenericError):
    """Generics class error."""

    pass


class GenericInstanceError(GenericError):
    """Generics instance error."""

    pass
