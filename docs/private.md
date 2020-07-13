# Private

## Why

Object-oriented programming has a lot of advantages over procedural programming.
The one of these advantages is encapsulation of data. In python
[encapsulation](<https://en.wikipedia.org/wiki/Encapsulation_(computer_programming)>)
is implemented without
[information hiding](https://en.wikipedia.org/wiki/Information_hiding). We lack
this feature and want to fix it.

### Leading underscores

The naming convention with leading underscores from
[pep8](https://www.python.org/dev/peps/pep-0008/#descriptive-naming-styles) does
not work the way we want. For example, the code below will not hide class
attributes.

```python

>>> class User:
...     def __init__(self, name):
...         self._name = name
...
...     def greet(self):
...         return f'Hello, {self._name}'

>>> user = User('Jeff')

>>> user.greet()
'Hello, Jeff'

>>> user._name  # No information hiding here :(
'Jeff'

```

It may be a nice convention to have it in the code base, but

- it does not work (it does not make architecture any better)
- it harms readability (underscores are ugly)

## Principles

- [All methods are public](#all-methods-are-public)
- [All attributes are private and hidden](#all-attributes-are-private-and-hidden)

### All methods are public

The main purpose of objects in object-oriented programming is in **behavior**
they could provide to the client code.

Behavior intended by object could be expressed with its methods.

Thus every instance and class method of the object is public. Class should be
decorated with `@private` function.

```python tab="attrs"

>>> from attr import attrs, attrib
>>> from generics import private

>>> @private
... @attrs(frozen=True)
... class User:
...     name = attrib()
...
...     def greet(self):
...         return f'Hello, {self.name}'

>>> User
Private(User)

>>> user = User('Jeff')
>>> user
Private(User(name='Jeff'))

>>> user.greet()
'Hello, Jeff'

```

```python tab="dataclasses"

>>> from dataclasses import dataclass
>>> from generics import private

>>> @private
... @dataclass(frozen=True)
... class User:
...     name: str
...
...     def greet(self):
...         return f'Hello, {self.name}'

>>> User
Private(User)

>>> user = User('Jeff')
>>> user
Private(User(name='Jeff'))

>>> user.greet()
'Hello, Jeff'

```

```python tab="pydantic"

>>> from pydantic import BaseModel
>>> from generics import private

>>> @private
... class User(BaseModel):
...     name: str
...
...     class Config:
...         allow_mutation = False
...
...     def greet(self):
...         return f'Hello, {self.name}'

>>> User
Private(User)

>>> user = User(name='Jeff')
>>> user
Private(User(name='Jeff'))

>>> user.greet()
'Hello, Jeff'

```

### All attributes are private and hidden

The main advantage of objects in object-oriented programming is in encapsulation
and **information hiding**.

Procedural programming have a lot of problems related to coupling. All data
flows directly through the execution flow. Every part of the code in this flow
is highly coupled with each other because of the data they pass to each other.

In opposite in the object-oriented programming we put parts of the data close to
the parts of the code where it'll be used. Thus the execution flow sees only
method calls. Client code does not know what data were encapsulated inside the
object. And it's none of its business.

Thus all attributes encapsulated inside the objects are private. The constructor
is the only place where you can put anything inside the object. Own methods of
the object (defined in its class) are free to use its attributes as usual.
Attribute access in the client code will raise an exception.

```python

>>> user.name
Traceback (most recent call last):
  ...
AttributeError: 'Private(User)' object has no attribute 'name'

```
