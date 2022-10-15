"""Tests related to the @private decorator."""
from datetime import date

import pytest

from generics import private
from generics.exceptions import GenericClassError


def test_allow_method_access(e):
    """All methods should be public."""
    user_class = private(e.User)
    user = user_class(last_login=date(1999, 12, 31))
    assert not user.is_active()


def test_deny_attribute_access(e):
    """All attributes should be private."""
    user_class = private(e.User)
    user = user_class(last_login=date.today())
    with pytest.raises(AttributeError) as exc_info:
        user.last_login
    expected = "'Private::User' object has no attribute 'last_login'"
    assert str(exc_info.value) == expected


def test_deny_magic_attribute_access(e):
    """Bound methods should not expose private attributes."""
    user_class = private(e.User)
    user = user_class(last_login=date.today())
    with pytest.raises(AttributeError):
        user.is_active.__self__.last_login


def test_instance_method_return_class_instance(e):
    """Instances returned from methods should be @private as well."""
    user_class = private(e.NamedUser)
    user = user_class(name="John").rename("Kate")
    assert user.greet() == "Hello, Kate"
    with pytest.raises(AttributeError) as exc_info:
        user.name
    expected = "'Private::NamedUser' object has no attribute 'name'"
    assert str(exc_info.value) == expected


def test_instance_method_should_not_work_with_class(e):
    """Deny to call instance methods using class attribute access."""
    user_class = private(e.User)
    with pytest.raises(GenericClassError) as exc_info:
        user_class.is_active()
    expected = "Instance methods can not be called on classes"
    assert str(exc_info.value) == expected


def test_require_at_least_one_instance_method(e):
    """Check decorated class has at least one instance method.

    Otherwise, encapsulated properties can not be used.  So there is no point to
    encapsulate them in the first place.

    """
    with pytest.raises(GenericClassError) as exc_info:
        private(e.NoMethodsUser)
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


def test_deny_keyword_encapsulated_attributes(e):
    """Deny double star arguments in class constructor."""
    with pytest.raises(GenericClassError) as exc_info:
        private(e.KwArgsUser)
    assert str(exc_info.value) == "Class could not have keyword encapsulated attribute"


def test_deny_static_method(e):
    """Deny static methods on classes."""
    with pytest.raises(GenericClassError) as exc_info:
        private(e.StaticMethodUser)
    assert str(exc_info.value) == "Do not use static methods (use composition instead)"


def test_deny_class_method(e):
    """Deny class methods on classes."""
    with pytest.raises(GenericClassError) as exc_info:
        private(e.ClassMethodUser)
    assert str(exc_info.value) == "Do not use class methods (call constructor instead)"


def test_deny_inheritance(e):
    """Deny inheritance on classes."""
    with pytest.raises(GenericClassError) as exc_info:
        private(e.InheritanceUser)
    assert str(exc_info.value) == "Do not use inheritance (use composition instead)"


def test_deny_private_method(e):
    """Deny private methods with leading underscore."""
    with pytest.raises(GenericClassError) as exc_info:
        private(e.UnderscoreMethodUser)
    assert str(exc_info.value) == "Do not use private methods (use composition instead)"


def test_deny_private_attribute(e):
    """Deny private attributes with leading underscore."""
    if not hasattr(e, "UnderscoreAttributeUser"):
        pytest.skip("Declaration does not support private attributes")
    with pytest.raises(GenericClassError) as exc_info:
        private(e.UnderscoreAttributeUser)
    assert str(exc_info.value) == "Do not use private attributes"


def test_deny_class_attribute(e):
    """Deny attributes defined on class."""
    with pytest.raises(GenericClassError) as exc_info:
        private(e.ClassAttributeUser)
    assert str(exc_info.value) == "Do not define attributes on classes"


def test_class_representation(e):
    """Origin class name should appears in the class representation."""
    user_class = private(e.User)
    user = user_class(last_login=date.today())
    assert "Private::User" == repr(user_class)
    assert "Private::User" == repr(user.__class__)


def test_instance_representation(e):
    """Origin instance representation should appears in the representation."""
    user_class = private(e.User)
    user = user_class(last_login=date.today())
    origin = e.User(last_login=date.today())
    assert f"Private::{origin!r}" == repr(user)


def test_method_class_representation(e):
    """Origin method name should appears in the class method representation."""
    user_class = private(e.User)
    assert "Private::User.is_active" == repr(user_class.is_active)


def test_method_instance_representation(e):
    """Origin method name should appears in the method name."""
    user_class = private(e.User)
    user = user_class(last_login=date.today())
    origin = e.User(last_login=date.today())
    assert f"Private::{origin!r}.is_active" == repr(user.is_active)
