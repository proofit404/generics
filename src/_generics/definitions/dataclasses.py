import dataclasses
import inspect


def _is_dataclass(entity):
    return inspect.isclass(entity) and dataclasses.is_dataclass(entity)


def _get_fields(entity):
    return [field.name for field in dataclasses.fields(entity)]


def _get_bases():
    return (object,)


def _get_init_method(entity):
    return entity.__dict__["__init__"]
