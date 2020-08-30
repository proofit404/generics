from types import FunctionType
from types import MethodType

from _generics.entities import _get_fields
from _generics.exceptions import GenericClassError
from _generics.exceptions import GenericInstanceError


def private(cls):
    """Create class with private attributes."""
    class_name = _get_class_name(cls)
    methods = _get_methods(cls)
    fields, bases, init = _get_fields(cls)
    _check_bases(cls, bases)
    _check_static_methods(cls, methods)
    _check_defined_methods(cls, methods)
    _check_defined_fields(fields)
    _check_private_methods(methods)
    _check_private_fields(fields)
    created_methods = _create_class_methods(cls, class_name, methods)
    created_methods["__new__"] = _create_new_class_method(cls, class_name, methods)
    created_methods["__init__"] = init
    return _PrivateType(class_name, (object,), created_methods)


def _get_class_name(cls):
    return "Private(" + cls.__name__ + ")"


def _get_methods(cls):
    return [attrname for attrname in cls.__dict__ if _is_method(cls, attrname)]


def _check_bases(cls, allowed_bases):
    if cls.__bases__ != allowed_bases:
        raise GenericClassError("Do not use inheritance (use composition instead)")


def _check_static_methods(cls, methods):
    for method in methods:
        if isinstance(cls.__dict__[method], staticmethod):
            message = "Do not use static methods (use composition instead)"
            raise GenericClassError(message)


def _check_defined_methods(cls, methods):
    instance_methods = [
        method
        for method in methods
        if not isinstance(cls.__dict__[method], classmethod)
    ]
    if not instance_methods:
        raise GenericClassError("Define at least one instance method")


def _check_defined_fields(fields):
    if not fields:
        raise GenericClassError("Define at least one encapsulated attribute")


def _check_private_methods(methods):
    if any(filter(lambda method: method.startswith("_"), methods)):
        raise GenericClassError("Do not use private methods (use composition instead)")


def _check_private_fields(fields):
    if any(filter(lambda field: field.startswith("_"), fields)):
        raise GenericClassError("Do not use private attributes")


def _create_class_methods(cls, class_name, methods):
    return {
        method: _create_class_method(cls, method, class_name, methods)
        for method in methods
    }


def _create_new_class_method(cls, class_name, methods):
    def method(_, *args, **kwargs):
        instance = cls(*args, **kwargs)
        return _wrap(instance, class_name, methods)

    method.__name__ = "__new__"
    return method


class _PrivateType(type):
    def __repr__(cls):
        return cls.__name__


def _is_method(cls, attrname):
    return not _is_dunder(attrname) and _is_method_type(cls, attrname)


def _is_dunder(name):
    return name.startswith("__") and name.endswith("__")


def _is_method_type(cls, attrname):
    return isinstance(getattr(cls, attrname), (FunctionType, MethodType))


def _create_class_method(cls, method_name, class_name, methods):
    if isinstance(cls.__dict__[method_name], classmethod):
        return _define_class_method_on_class(cls, method_name, class_name, methods)
    else:
        return _define_instance_method_on_class(method_name)


def _define_class_method_on_class(cls, method_name, class_name, methods):
    def method(_, *args, **kwargs):
        result = getattr(cls, method_name)(*args, **kwargs)
        if type(result) is cls:
            return _wrap(result, class_name, methods)
        else:
            template = "{!r} classmethod should return an instance of the {!r} class"
            message = template.format(method_name, cls.__name__)
            raise GenericInstanceError(message)

    method.__name__ = method_name
    return classmethod(method)


def _define_instance_method_on_class(method_name):
    def method(*args, **kwargs):
        message = "Use instance attribute access to invoke instance methods"
        raise GenericInstanceError(message)

    method.__name__ = method_name
    return method


def _wrap(instance, class_name, methods):
    created_methods = {method: _create_method(instance, method) for method in methods}
    created_methods["__repr__"] = _create_repr_method(instance)
    return type(class_name, (object,), created_methods)()


def _create_method(instance, method_name):
    def method(_, *args, **kwargs):
        return getattr(instance, method_name)(*args, **kwargs)

    method.__name__ = method_name
    return method


def _create_repr_method(instance):
    def method(_):
        return "Private(" + repr(instance) + ")"

    method.__name__ = "__repr__"
    return method
