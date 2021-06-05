# Dependencies

It is possible to instantiate classes decorated with `@private` function via
[dependencies](https://proofit404.github.io/dependencies/) library.

```pycon

>>> from dependencies import Injector
>>> from generics import private

>>> @private
... class User:
...     def __init__(self, name):
...         self.name = name
...
...     def greet(self):
...         return f"Hello, {self.name}"

>>> class UserContainer(Injector):
...     user = User
...     name = "Jeff"

>>> UserContainer.user.greet()
'Hello, Jeff'

```

<p align="center">&mdash; ⭐ &mdash;</p>
<p align="center"><i>The <code>generics</code> library is part of the SOLID python family.</i></p>
