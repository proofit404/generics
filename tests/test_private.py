"""Tests related to the @private decorator."""
from datetime import datetime

import pytest

from generics import private
from generics.exceptions import GenericClassError
from generics.exceptions import GenericInstanceError


instantiate_strategy = pytest.mark.parametrize(
    "strategy", [lambda c: c(last_login=datetime.now()), lambda c: c.new()]
)


def test_allow_method_access(e):
    """All methods should be public."""
    user_class = private(e.User)
    user = user_class(last_login=datetime(1999, 12, 31))
    assert not user.is_active()


@instantiate_strategy
def test_deny_attribute_access(e, strategy):
    """All attributes should be private."""
    user_class = private(e.User)
    user = strategy(user_class)
    with pytest.raises(AttributeError):
        user.last_login


@instantiate_strategy
def test_deny_magic_attribute_access(e, strategy):
    """Bound methods should not expose private attributes."""
    user_class = private(e.User)
    user = strategy(user_class)
    with pytest.raises(AttributeError):
        user.is_active.__self__.last_login


@pytest.mark.parametrize("method_name", ["is_bot", "new_bot"])
def test_class_method_should_return_class_instance(e, method_name):
    """Deny to return arbitrary data from class methods."""
    bot_class = private(e.Bot)
    with pytest.raises(GenericInstanceError) as exc_info:
        getattr(bot_class, method_name)()
    template = "{!r} classmethod should return an instance of the 'Bot' class"
    expected = template.format(method_name)
    assert str(exc_info.value) == expected


@instantiate_strategy
def test_class_method_should_not_work_with_instance(e, strategy):
    """Deny to call class methods using instance attribute access."""
    user_class = private(e.User)
    user = strategy(user_class)
    with pytest.raises(GenericInstanceError) as exc_info:
        user.new()
    expected = "Class methods can not be called on instances"
    assert str(exc_info.value) == expected


def test_instance_method_should_not_work_with_class(e):
    """Deny to call instance methods using class attribute access."""
    user_class = private(e.User)
    with pytest.raises(GenericClassError) as exc_info:
        user_class.is_active()
    expected = "Instance methods can not be called on classes"
    assert str(exc_info.value) == expected


@pytest.mark.parametrize("class_name", ["NoMethodsUser", "ClassMethodOnlyUser"])
def test_require_at_least_one_instance_method(e, class_name):
    """Check decorated class has at least one instance method.

    Otherwise, encapsulated properties can not be used.  So there is no point to
    encapsulate them in the first place.

    """
    with pytest.raises(GenericClassError) as exc_info:
        private(getattr(e, class_name))
    assert str(exc_info.value) == "Define at least one instance method"


def test_require_at_least_one_encapsulated_attribute(e):
    """Check decorated class has at least one encapsulated attribute.

    Otherwise, instance methods will be actually static methods.

    """
    with pytest.raises(GenericClassError) as exc_info:
        private(e.NoEncapsulationUser)
    assert str(exc_info.value) == "Define at least one encapsulated attribute"


def test_deny_variable_encapsulated_attributes(e):
    """Deny star arguments in class constructor."""
    with pytest.raises(GenericClassError) as exc_info:
        private(e.VarArgsUser)
    assert str(exc_info.value) == "Class could not have variable encapsulated attribute"


def test_deny_static_method(e):
    """Deny static methods on classes."""
    with pytest.raises(GenericClassError) as exc_info:
        private(e.StaticBot)
    assert str(exc_info.value) == "Do not use static methods (use composition instead)"


def test_deny_inheritance(e):
    """Deny inheritance on classes."""
    with pytest.raises(GenericClassError) as exc_info:
        private(e.InheritanceUser)
    assert str(exc_info.value) == "Do not use inheritance (use composition instead)"


@pytest.mark.parametrize(
    "class_name",
    [
        "UnderscoreMethodUser",
        "DoubleUnderscoreMethodUser",
        "UnderscoreClassMethodUser",
        "DoubleUnderscoreClassMethodUser",
    ],
)
def test_deny_private_method(e, class_name):
    """Deny private methods with leading underscore."""
    with pytest.raises(GenericClassError) as exc_info:
        private(getattr(e, class_name))
    assert str(exc_info.value) == "Do not use private methods (use composition instead)"


@instantiate_strategy
def test_global_methods(e, strategy):
    """Allow private methods defined in global scope.

    This rules applies to cases if function with private name stored in public
    attribute.

    """
    user_class = private(e.GlobalMethodUser)
    user = strategy(user_class)
    assert user.is_active()


def test_deny_private_attribute(e):
    """Deny private attributes with leading underscore."""
    with pytest.raises(GenericClassError) as exc_info:
        private(e.UnderscoreAttributeUser)
    assert str(exc_info.value) == "Do not use private attributes"


@instantiate_strategy
@pytest.mark.parametrize("class_name", ["DunderMethodUser", "DunderClassMethodUser"])
def test_dunder_method(e, strategy, class_name):
    """Ignore methods defined with dunder name.

    This is not supposed to be a publicly documented principle. It's necessary for
    third-party libraries support which may assign their own dunder attributes for some
    internal needs.

    """
    user_class = private(getattr(e, class_name))
    user = strategy(user_class)
    assert user.is_active()


@instantiate_strategy
def test_class_name(e, strategy):
    """Origin class name should appears in the class name."""
    user_class = private(e.User)
    user = strategy(user_class)
    assert "Private(User)" == user_class.__name__
    assert "Private(User)" == user.__class__.__name__


def test_class_method_name(e):
    """Origin method name should appears in the class method name."""
    user_class = private(e.User)
    assert "__new__" == user_class.__new__.__name__
    assert "new" == user_class.new.__name__
    assert "is_active" == user_class.is_active.__name__


@instantiate_strategy
def test_method_name(e, strategy):
    """Origin method name should appears in the method name."""
    user_class = private(e.User)
    user = strategy(user_class)
    assert "new" == user.new.__name__
    assert "is_active" == user.is_active.__name__
    assert "__repr__" == user_class.__repr__.__name__
    assert "__repr__" == user.__class__.__repr__.__name__
    assert "__repr__" == user.__repr__.__name__


@instantiate_strategy
def test_class_method_type(e, strategy):
    """Origin method types should be kept in the decorated class."""
    user_class = private(e.User)
    assert isinstance(user_class.__dict__["new"], classmethod)
    assert not isinstance(user_class.__dict__["is_active"], classmethod)
    user = strategy(user_class)
    assert isinstance(user.__class__.__dict__["new"], classmethod)
    assert not isinstance(user.__class__.__dict__["is_active"], classmethod)


def test_class_representation(e):
    """Origin class name should appears in the class representation."""
    user_class = private(e.User)
    assert "Private(User)" == repr(user_class)


def test_instance_representation(e):
    """Origin instance representation should appears in the representation."""
    last_login = datetime.now()
    user_class = private(e.User)
    user = user_class(last_login=last_login)
    origin_user = e.User(last_login=last_login)
    expected = "Private(" + repr(origin_user) + ")"
    assert expected == repr(user)
