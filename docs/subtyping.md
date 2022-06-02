# Interface subtyping

## Why

## Principles

- [Inheritance from interface is allowed](#inheritance-from-interface-is-allowed)

### Inheritance from interface is allowed

Python has builtin support for
[subtype polymorphism](https://en.wikipedia.org/wiki/Subtyping) (or inclusion
polymorphism) via [ABC](https://docs.python.org/3/library/abc.html) library.
It's syntax is based on defining an interface (or abstract class) and then
inherit from it (implement interface).

Personally, we dislike such syntax and would prefer `@implements` decorator or
something similar to `zope.interface`. But default `ABC` library is widely
supported by type checkers (like mypy) and language servers (reference search).
That's why we decided not to reinvent our own wheel.

We allow classes decorated by `@private` and `@delegated` decorators inherit
from interfaces (`abc.ABC` subclasses) with some additional restrictions. See
below.

```pycon

>>> from abc import ABC, abstractmethod
>>> from generics import private

>>> class User(ABC):
...     @abstractmethod
...     def greet(self):
...         ...

>>> @private
... class ConsoleUser(User):
...     def greet(self):
...         print(f"Hello, {self.name}")
...
...     def __init__(self, name):
...         self.name = name

>>> ConsoleUser("Jeff").greet()
Hello, Jeff

```

Default restrictions forced by `abc` library would apply as usual. For example,
You have to implement all `@abstractmethod`s to instantiate the class.

```pycon

>>> @private
... class Bot(User):
...     def ping(self):
...         urllib.open(self.ip)
...
...     def __init__(self, ip):
...         self.ip = ip

>>> Bot("127.0.0.1")
Traceback (most recent call last):
  ...
TypeError: Can't instantiate abstract class Bot with abstract method greet

```

<p align="center">&mdash; ⭐ &mdash;</p>
