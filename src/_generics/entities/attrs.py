import inspect

try:
    import attr

    IS_AVAILABLE = True
except ImportError:  # pragma: no cover
    IS_AVAILABLE = False


def _is_attrs(entity):
    if IS_AVAILABLE:
        return inspect.isclass(entity) and attr.has(entity)
    else:
        return False  # pragma: no cover


def _get_fields(entity):
    return [attribute.name for attribute in entity.__attrs_attrs__]


def _get_bases():
    return (object,)


def _get_init_method(entity):
    return entity.__dict__["__init__"]
