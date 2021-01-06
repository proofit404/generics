# Pydantic

[pydantic](https://pydantic-docs.helpmanual.io/) is a popular library for data
validation. It could be used to define business entities of your domain if you
want validation to be applied to data your entities encapsulate. It's possible
to use a third-party library `pydantic-initialized` to make defined models
compatible with `generics` library decorators. As with all previous examples we
advice you to make your instances immutable. `pydantic` library has a first
class support for immutability. Disable `allow_mutation` setting on model config
and use `copy` method of the instance.

```pycon

>>> from generics import private
>>> from pydantic import BaseModel
>>> from pydantic_initialized import initialized

>>> @private
... @initialized
... class User(BaseModel):
...     name: str
...
...     class Config:
...         allow_mutation = False
...
...     def greet(self):
...         return f'Hello, {self.name}'
...
...     def rename(self, name):
...         return self.copy(update={'name': name})

>>> User
Private(User)

>>> user = User(name='Jeff')
>>> user
Private(User(name='Jeff'))

>>> user.greet()
'Hello, Jeff'

>>> user.rename('Kate')
User(name='Kate')

```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The generics library is part of the SOLID python family.</i></p>
