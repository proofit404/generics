# Attrs

[attrs](https://www.attrs.org/en/stable/) is a well known library to define
classes in a nicer & shorter way. `generics` library works out of the box with
`attrs`. As with all previous examples we advice you to make your instances
immutable. `attrs` library has a first class support for immutability. Enable
`frozen` setting on class and use `evolve` function to copy instancies of it.

```pycon

>>> from attr import attrs, attrib, evolve
>>> from generics import private

>>> @private
... @attrs(frozen=True)
... class User:
...     name = attrib()
...
...     def greet(self):
...         return f'Hello, {self.name}'
...
...     def rename(self, name):
...         return evolve(self, name=name)

>>> User
Private(User)

>>> user = User('Jeff')
>>> user
Private(User(name='Jeff'))

>>> user.greet()
'Hello, Jeff'

>>> user.rename('Kate')
User(name='Kate')

```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The generics library is part of the SOLID python family.</i></p>
