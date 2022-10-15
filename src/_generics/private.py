from inspect import signature
from types import MemberDescriptorType

from _generics.exceptions import GenericClassError


def private(cls):
    """Create class with private attributes."""
    methods = _get_methods(cls)
    init = _get_init(cls)
    fields = _get_fields(init)
    _check_bases(cls)
    _check_methods(methods)
    _check_fields(fields)
    _check_private_methods(methods)
    _check_private_fields(fields)
    _check_variable_keyword_fields(fields)
    _check_variable_positional_fields(fields)
    class_name = _get_class_name(cls)
    defined = _define_class_methods(methods)
    defined["__new__"] = _define_new_class_method(cls, methods)
    defined["__init__"] = init
    return _PrivateType(class_name, (), defined)


def _get_methods(cls):
    methods = []
    for name, attribute in cls.__dict__.items():
        method = _get_method(cls, name, attribute)
        if method:
            methods.append(method)
    return methods


def _get_init(cls):
    return cls.__dict__.get("__init__")


def _get_fields(init):
    if init is None:
        return []
    params = iter(signature(init).parameters.items())
    next(params)  # Skip self constructor argument.
    return [_get_field_name(name, param) for name, param in params]


def _get_field_name(name, param):
    if param.kind is param.VAR_POSITIONAL:
        return f"*{name}"
    elif param.kind is param.VAR_KEYWORD:
        return f"**{name}"
    else:
        return name


def _check_bases(cls):
    if cls.__bases__ != (object,):
        raise GenericClassError("Do not use inheritance (use composition instead)")


def _check_methods(methods):
    if not methods:
        raise GenericClassError("Define at least one instance method")


def _check_fields(fields):
    if not fields:
        raise GenericClassError("Define at least one encapsulated attribute")


def _check_private_methods(methods):
    for method in methods:
        if method.name.startswith("_"):
            raise GenericClassError(
                "Do not use private methods (use composition instead)"
            )


def _check_private_fields(fields):
    for field in fields:
        if field.startswith("_"):
            raise GenericClassError("Do not use private attributes")


def _check_variable_keyword_fields(fields):
    for field in fields:
        if field.startswith("**"):
            raise GenericClassError(
                "Class could not have keyword encapsulated attribute"
            )


def _check_variable_positional_fields(fields):
    for field in fields:
        if field.startswith("*"):
            raise GenericClassError(
                "Class could not have variable encapsulated attribute"
            )


def _define_class_methods(methods):
    return {method.name: method.to_class(methods) for method in methods}


def _define_instance_methods(instance, methods):
    return {method.name: method.to_instance(instance, methods) for method in methods}


def _define_new_class_method(cls, methods):
    def method(_, *args, **kwargs):
        instance = cls(*args, **kwargs)
        return _wrap(instance, methods)

    return method


def _define_repr_instance_method(instance):
    def method(_):
        return f"Private::{instance!r}"

    return method


def _wrap(instance, methods):
    class_name = _get_class_name(instance.__class__)
    defined = _define_instance_methods(instance, methods)
    defined["__repr__"] = _define_repr_instance_method(instance)
    return _PrivateType(class_name, (), defined)()


def _get_class_name(cls):
    return f"Private::{cls.__name__}"


class _PrivateType(type):
    def __repr__(cls):
        return cls.__name__


def _get_method(cls, name, attribute):
    if not _is_dunder(name):
        return (
            _deny_static_method(attribute)
            or _deny_class_method(attribute)
            or _get_instance_method(cls, name, attribute)
            or _deny_class_attribute(attribute)
        )


def _deny_static_method(attribute):
    if isinstance(attribute, staticmethod):
        message = "Do not use static methods (use composition instead)"
        raise GenericClassError(message)


def _deny_class_method(attribute):
    if isinstance(attribute, classmethod):
        message = "Do not use class methods (call constructor instead)"
        raise GenericClassError(message)


def _get_instance_method(cls, name, attribute):
    if callable(attribute):
        return _Method(cls, name, attribute)


def _deny_class_attribute(attribute):
    if not isinstance(attribute, MemberDescriptorType):
        raise GenericClassError("Do not define attributes on classes")


def _is_dunder(name):
    return name.startswith("__") and name.endswith("__")  # pragma: no mutate


class _Method:
    def __init__(self, cls, name, func):
        self.cls = cls
        self.name = name
        self.func = func

    def to_class(self, methods):
        class Method:
            def __call__(_, *args, **kwargs):
                message = "Instance methods can not be called on classes"
                raise GenericClassError(message)

            def __repr__(_):
                return f"Private::{self.cls.__name__}.{self.name}"

        return Method()

    def to_instance(self, instance, methods):
        class Method:
            def __call__(_, *args, **kwargs):
                result = self.func(instance, *args, **kwargs)
                if type(result) is self.cls:
                    result = _wrap(result, methods)
                return result

            def __repr__(_):
                return f"Private::{instance!r}.{self.name}"

        return Method()
