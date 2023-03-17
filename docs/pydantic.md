# Pydantic

[pydantic](https://pydantic-docs.helpmanual.io/) is a popular library for data
validation. It could be used to define business entities of your domain if you
want validation to be applied to data your entities encapsulate. It's possible
to use a
[pydantic dataclasses](https://pydantic-docs.helpmanual.io/usage/dataclasses/)
to make defined entities compatible with `generics` library decorators. As with
all previous examples we advice you to make your instances immutable. `pydantic`
library has a first class support for immutability. Enable `frozen` setting on
class and use `replace` function to copy instancies of it.

```pycon

>>> from pydantic.dataclasses import dataclass
>>> from dataclasses import replace
>>> from generics import private

>>> @private
... @dataclass(frozen=True)
... class User:
...     name: str
...
...     def greet(self):
...         return f"Hello, {self.name}"
...
...     def rename(self, name):
...         return replace(self, name=name)

>>> User
Private::User

>>> user = User("Jeff")
>>> user
Private::User(name='Jeff')

>>> user.greet()
'Hello, Jeff'

>>> user.rename("Kate")
Private::User(name='Kate')

```

Arguments validation would be applied at the object construction time. This
behavior would match regular dataclasses created by `pydantic`.

```pycon

>>> from typing import Callable

>>> @private
... @dataclass(frozen=True)
... class User:
...     name: str
...     console: Callable
...
...     def greet(self):
...         self.console(f'Hello, {self.name}')

>>> User(name='Jeff', console=print)
Private::User(name='Jeff', console=<built-in function print>)

>>> User(name='Jeff', console=True)
Traceback (most recent call last):
  ...
pydantic.error_wrappers.ValidationError: 1 validation error for User
console
  True is not callable (type=type_error.callable; value=True)

```
