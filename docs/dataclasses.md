# Dataclasses

[dataclasses](https://docs.python.org/3/library/dataclasses.html) is a simpler
alternative to `attrs` from python standard library. `generics` works with it
out of the box. As with all previous examples we advice you to make your
instances immutable. `dataclasses` library has a first class support for
immutability. Enable `frozen` setting on class and use `replace` function to
copy instancies of it.

```pycon

>>> from dataclasses import dataclass, replace
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
Private(User)

>>> user = User("Jeff")
>>> user
Private(User(name='Jeff'))

>>> user.greet()
'Hello, Jeff'

>>> user.rename("Kate")
User(name='Kate')

```

<p align="center">&mdash; ⭐ &mdash;</p>
