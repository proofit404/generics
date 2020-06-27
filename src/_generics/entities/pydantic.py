# -*- coding: utf-8 -*-
from __future__ import absolute_import

import inspect


try:
    import pydantic

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def _is_pydantic(entity):
    if IS_AVAILABLE:
        return inspect.isclass(entity) and issubclass(entity, pydantic.main.BaseModel)
    else:
        return False


def _get_fields(entity):
    return list(entity.__fields__)


def _get_bases():
    return (pydantic.main.BaseModel,)
