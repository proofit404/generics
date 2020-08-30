import inspect


try:
    import pydantic

    IS_AVAILABLE = True
except ImportError:  # pragma: no cover
    IS_AVAILABLE = False


def _is_pydantic(entity):
    if IS_AVAILABLE:
        return inspect.isclass(entity) and issubclass(entity, pydantic.main.BaseModel)
    else:
        return False  # pragma: no cover


def _get_fields(entity):
    return list(entity.__fields__)


def _get_bases():
    return (pydantic.main.BaseModel,)


def _get_init_method(entity):
    return pydantic.main.BaseModel.__dict__["__init__"]
