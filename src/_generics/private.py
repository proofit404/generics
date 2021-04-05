from inspect import signature

from _generics.exceptions import GenericClassError
from _generics.exceptions import GenericInstanceError


def private(cls):
    """Create class with private attributes."""
    class_name = _get_class_name(cls)
    methods = _get_methods(cls)
    init = _get_init_method(cls)
    fields = _get_fields(init)
    _check_bases(cls)
    _check_defined_methods(methods)
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
    structures = [
        _method_structure(cls, attribute_name, attribute)
        for attribute_name, attribute in cls.__dict__.items()
    ]
    return [structure for structure in structures if structure]


def _get_init_method(cls):
    return cls.__dict__.get("__init__")


def _get_fields(init):
    if init is not None:
        return list(signature(init).parameters)[1:]
    else:
        return []


def _check_bases(cls):
    if cls.__bases__ != (object,):
        raise GenericClassError("Do not use inheritance (use composition instead)")


def _check_defined_methods(methods):
    instance_methods = [method for method in methods if method.is_instance_method()]
    if not instance_methods:
        raise GenericClassError("Define at least one instance method")


def _check_defined_fields(fields):
    if not fields:
        raise GenericClassError("Define at least one encapsulated attribute")


def _check_private_methods(methods):
    private_methods = [method for method in methods if method.is_private_method()]
    if private_methods:
        raise GenericClassError("Do not use private methods (use composition instead)")


def _check_private_fields(fields):
    private_fields = [field for field in fields if field.startswith("_")]
    if private_fields:
        raise GenericClassError("Do not use private attributes")


def _create_class_methods(cls, class_name, methods):
    return {
        method.name: _create_class_method(cls, method, class_name, methods)
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


def _method_structure(cls, attribute_name, attribute):
    return (
        _deny_static_method(attribute)
        or _class_method_structure(cls, attribute_name, attribute)
        or _instance_method_structure(cls, attribute_name, attribute)
    )


def _deny_static_method(attribute):
    if isinstance(attribute, staticmethod):
        message = "Do not use static methods (use composition instead)"
        raise GenericClassError(message)


def _class_method_structure(cls, attribute_name, attribute):
    if isinstance(attribute, classmethod):
        name = _choose_name(cls, attribute_name, attribute.__func__)
        if not _is_dunder(name):
            return _MethodStructure(False, name, attribute.__func__)


def _instance_method_structure(cls, attribute_name, attribute):
    if callable(attribute):
        name = _choose_name(cls, attribute_name, attribute)
        if not _is_dunder(name):
            return _MethodStructure(True, name, attribute)


def _choose_name(cls, attribute_name, func):
    if func.__qualname__.startswith(f"{cls.__name__}."):
        return func.__name__
    else:
        return attribute_name


def _is_dunder(name):
    return name.startswith("__") and name.endswith("__")


class _MethodStructure:
    def __init__(self, normal, name, func):
        self.normal = normal
        self.name = name
        self.func = func

    def is_instance_method(self):
        return self.normal is True

    def is_class_method(self):
        return self.normal is False

    def is_private_method(self):
        return self.name.startswith("_")


def _create_class_method(cls, method, class_name, methods):
    if method.is_class_method():
        return _define_class_method_on_class(cls, method, class_name, methods)
    else:
        return _define_instance_method_on_class(method)


def _define_class_method_on_class(cls, structure, class_name, methods):
    def method(_, *args, **kwargs):
        result = structure.func(cls, *args, **kwargs)
        if type(result) is cls:
            return _wrap(result, class_name, methods)
        else:
            template = "{!r} classmethod should return an instance of the {!r} class"
            message = template.format(structure.name, cls.__name__)
            raise GenericInstanceError(message)

    method.__name__ = structure.name
    return classmethod(method)


def _define_instance_method_on_class(structure):
    def method(*args, **kwargs):
        message = "Instance methods can not be called on classes"
        raise GenericClassError(message)

    method.__name__ = structure.name
    return method


def _wrap(instance, class_name, methods):
    created_methods = {
        method.name: _create_instance_method(instance, method) for method in methods
    }
    created_methods["__repr__"] = _create_repr_method(instance)
    return type(class_name, (object,), created_methods)()


def _create_instance_method(instance, structure):
    if structure.is_class_method():
        return _create_class_method_on_instance(structure)
    else:
        return _create_instance_method_on_instance(instance, structure)


def _create_class_method_on_instance(structure):
    def method(*args, **kwargs):
        message = "Class methods can not be called on instances"
        raise GenericInstanceError(message)

    method.__name__ = structure.name
    return classmethod(method)


def _create_instance_method_on_instance(instance, structure):
    def method(_, *args, **kwargs):
        return structure.func(instance, *args, **kwargs)

    method.__name__ = structure.name
    return method


def _create_repr_method(instance):
    def method(_):
        return "Private(" + repr(instance) + ")"

    method.__name__ = "__repr__"
    return method
