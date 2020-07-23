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
- [Static methods are forbidden](#static-methods-are-forbidden)
- [Class methods should return instances](#class-methods-should-return-instances)

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

### Static methods are forbidden

Good objects expose their behavior and hide their state. The behavior objects
expose should be related to the state object hides. This metric is called
cohesion.

Static methods can't access the inner state of the object. That's why the
behavior they expose doesn't relate to the object. Cohesion will go down. That's
why we forbid static methods.

If you need such behavior, put it outside of the class. If this behavior is
neccessary in the instance method of the original class, encapsulate it. Pass
that new thing to the constructor and access it in methods.

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
...
...     @staticmethod
...     def is_bot():
...         return False
Traceback (most recent call last):
  ...
_generics.exceptions.GenericClassError: Do not use static methods (use composition instead)

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
...
...     @staticmethod
...     def is_bot():
...         return False
Traceback (most recent call last):
  ...
_generics.exceptions.GenericClassError: Do not use static methods (use composition instead)

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
...
...     @staticmethod
...     def is_bot():
...         return False
Traceback (most recent call last):
  ...
_generics.exceptions.GenericClassError: Do not use static methods (use composition instead)

```

### Class methods should return instances

As we mentioned earlier, objects should expose behavior. Class methods do not
have access to any kind of inner state sinse there is no object encapsulating
it. Thus the only kind of behavior class method should be able to do is
instantiation of the object.

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
...
...     @classmethod
...     def create(cls):
...         pass

>>> User.create()
Traceback (most recent call last):
  ...
_generics.exceptions.GenericInstanceError: 'create' classmethod should return an instance of the 'User' class

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
...
...     @classmethod
...     def create(cls):
...         pass

>>> User.create()
Traceback (most recent call last):
  ...
_generics.exceptions.GenericInstanceError: 'create' classmethod should return an instance of the 'User' class

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
...
...     @classmethod
...     def create(cls):
...         pass

>>> User.create()
Traceback (most recent call last):
  ...
_generics.exceptions.GenericInstanceError: 'create' classmethod should return an instance of the 'User' class

```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The generics library is part of the SOLID python family.</i></p>
