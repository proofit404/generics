# -*- coding: utf-8 -*-
from _generics.entities import attrs
from _generics.entities import dataclasses
from _generics.entities import pydantic
from _generics.exceptions import GenericClassError


def _get_fields(entity):
    if dataclasses._is_dataclass(entity):
        fields = dataclasses._get_fields(entity)
        bases = dataclasses._get_bases()
        return fields, bases
    elif pydantic._is_pydantic(entity):
        fields = pydantic._get_fields(entity)
        bases = pydantic._get_bases()
        return fields, bases
    elif attrs._is_attrs(entity):
        fields = attrs._get_fields(entity)
        bases = attrs._get_bases()
        return fields, bases
    else:
        raise GenericClassError("Unknown type definition")
