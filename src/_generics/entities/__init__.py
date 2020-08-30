from _generics.entities import attrs
from _generics.entities import dataclasses
from _generics.entities import pydantic
from _generics.exceptions import GenericClassError


def _get_fields(entity):
    if dataclasses._is_dataclass(entity):
        fields = dataclasses._get_fields(entity)
        bases = dataclasses._get_bases()
        init = dataclasses._get_init_method(entity)
        return fields, bases, init
    elif pydantic._is_pydantic(entity):
        fields = pydantic._get_fields(entity)
        bases = pydantic._get_bases()
        init = pydantic._get_init_method(entity)
        return fields, bases, init
    elif attrs._is_attrs(entity):
        fields = attrs._get_fields(entity)
        bases = attrs._get_bases()
        init = attrs._get_init_method(entity)
        return fields, bases, init
    else:
        raise GenericClassError("Unknown type definition")
