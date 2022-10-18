# Delegate

## Why

Decorator is a powerful pattern in the OOP world. It means to adjust behavior of
the object, you suppose to encapsulate it inside another object. Adjusted
behavior would be implemented in methods of the decorator object itself.

However, there are a lot of challenges to make this pattern useful and easy when
you need it.

When you call methods of encapsulated object to execute original behavor of the
method, it means your object delegates responsibility to it.

### Attributes you didn't touch

Sometimes you don't need to override all of the encapsulated object methods.

Python language itself has nice mechanism of `__getattr__` method, where you
could return attributes which isn't defined on the instance itself.

Problem comes when you would try to use this mechanism with methods. Attribute
access should return bound method.

```pycon

>>> class User:
...     def __init__(self, name):
...         self._name = name
...
...     def __repr__(self):
...         return f"User({self._name=!r})"
...
...     def greet(self, prefix):
...         return f"{prefix}, {self._name}"

>>> class Decorator:
...     def __init__(self, user):
...         self._user = user
...
...     def __getattr__(self, name):
...         def boundmethod(*args, **kwargs):
...             print(f"=> {self._user}.{name}(*{args!r}, **{kwargs!r})")
...             method = getattr(self._user, name)
...             result = method(*args, **kwargs)
...             print(f"<= {self._user}.{name}: {result!r}")
...             return result
...
...         return boundmethod

>>> user = User("Jeff")
>>> user.greet("Hello")
'Hello, Jeff'

>>> decorated_user = Decorator(user)
>>> decorated_user.greet("Hello")
=> User(self._name='Jeff').greet(*('Hello',), **{})
<= User(self._name='Jeff').greet: 'Hello, Jeff'
'Hello, Jeff'

```

## Principles

- [Methods would be dispatched dynamically](#methods-would-be-dispatched-dynamically)

### Methods would be dispatched dynamically

When you need to adjust behavior only of a few methods of the class, there is no
point to write dumb boilerplate methods that would pass arguments as is to the
method of encapsulated object.

Methods of encapsulated object would be dispatched to the generic
implementation.

```pycon

>>> from generics import private, delegate

>>> @private
... class User:
...     def __init__(self, name):
...         self.name = name
...
...     def __repr__(self):
...         return f'User({self.name=!r})'
...
...     def greet(self):
...         return f'Hello, {self.name}'

>>> @private
... class Logged:
...     def __init__(self, instance):
...         self.instance = instance
...
...     @delegate
...     def log(self, name, args, kwargs):
...         print(f'=> {self.instance!r}.{name}(*{args!r}, **{kwargs!r})')
...         method = getattr(self.instance, name)
...         result = method(*args, **kwargs)
...         print(f'<= {method}: {result}')
...         return result

>>> user = User('Jeff')
>>> user.greet()
'Hello, Jeff'

>>> logged_user = Logged(User('Kate'))
>>> logged_user.greet()
=> Private::User(self.name='Kate').greet(*(), **{})
<= Private::User(self.name='Kate').greet: Hello, Kate
'Hello, Kate'

```

<p align="center">&mdash; ⭐ &mdash;</p>
