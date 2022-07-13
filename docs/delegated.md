# Delegated

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
...     def greet(self):
...         return f"Hello, {self._name}"

>>> class Decorator:
...     def __init__(self, user):
...         self._user = user
...
...     def __getattr__(self, name):
...         boundmethod = getattr(self._user)
...         return boundmethod

```

## Principles

- [Missing methods would be defined automatically](#missing-methods-would-be-defined-automatically)

### Missing methods would be defined automatically

When you need to adjust behavior only of a few methods of the class, there is no
point to write dumb boilerplate methods that would pass arguments as is to the
method of encapsulated object.

Methods of encapsulated object would be defined on the delegated class
automatically.

```pycon

>>> from datetime import date, timedelta
>>> from generics import private, delegated

>>> @private
... class User:
...     def __init__(self, name, last_login):
...         self.name = name
...         self.last_login = last_login
...
...     def greet(self):
...         return f'Hello, {self.name}'
...
...     def is_active(self):
...         return self.last_login >= date.today() - timedelta(days=30)

>>> @delegated(User)
... class LoggedUser:
...     def __init__(self, user):
...         self.user = user
...
...     def greet(self):
...         print(f'Greeting {self.user!r}')

>>> yesterday = date.today() - timedelta(days=1)
>>> month_ago = date.today() - timedelta(days=31)

>>> user = User('Jeff', yesterday)
>>> user.greet()
'Hello, Jeff'
>>> user.is_active()
True

>>> logged_user = LoggedUser(User('Kate', month_ago))
>>> logged_user.is_active()
False

```

<p align="center">&mdash; ⭐ &mdash;</p>
