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

```pycon

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
- [At least one instance method is required](#at-least-one-instance-method-is-required)
- [At least one encapsulated attribute is required](#at-least-one-encapsulated-attribute-is-required)
- [Implementation inheritance is forbidden](#implementation-inheritance-is-forbidden)
- [Underscore names are forbidden](#underscore-names-are-forbidden)
- [Prefer immutable classes](#prefer-immutable-classes)

### All methods are public

The main purpose of objects in object-oriented programming is in **behavior**
they could provide to the client code.

Behavior intended by object could be expressed with its methods.

Thus every instance and class method of the object is public. Class should be
decorated with `@private` function.

=== "attrs"

    ```pycon

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

=== "dataclasses"

    ```pycon

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

=== "pydantic"

    ```pycon

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

```pycon

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

=== "attrs"

    ```pycon

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

=== "dataclasses"

    ```pycon

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

=== "pydantic"

    ```pycon

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

=== "attrs"

    ```pycon

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

=== "dataclasses"

    ```pycon

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

=== "pydantic"

    ```pycon

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

### At least one instance method is required

As we mention a couple of times earlier the main goal of the good objects is to
expose behavior. If there is no methods defined on the class, it's not possible
to expose any kind of behavior. The object becomes useless.

Class methods does not count since it has a different purpose.

=== "attrs"

    ```pycon

    >>> from attr import attrs, attrib
    >>> from generics import private

    >>> @private
    ... @attrs(frozen=True)
    ... class User:
    ...     name = attrib()
    ...
    ...     @classmethod
    ...     def create(cls):
    ...         pass
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Define at least one instance method

    ```

=== "dataclasses"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from generics import private

    >>> @private
    ... @dataclass(frozen=True)
    ... class User:
    ...     name: str
    ...
    ...     @classmethod
    ...     def create(cls):
    ...         pass
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Define at least one instance method

    ```

=== "pydantic"

    ```pycon

    >>> from pydantic import BaseModel
    >>> from generics import private

    >>> @private
    ... class User(BaseModel):
    ...     name: str
    ...
    ...     class Config:
    ...         allow_mutation = False
    ...
    ...     @classmethod
    ...     def create(cls):
    ...         pass
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Define at least one instance method

    ```

### At least one encapsulated attribute is required

The same as a previous one this rules exists because of the encapsulation
restrictions. If your object does not encapsulate at least one attribute, it
does not have any state. In that case behavior exposed by the object does not
relate to the object itself. Thus there is no reason to define such kind of
method on the class in the first place.

=== "attrs"

    ```pycon

    >>> from attr import attrs, attrib
    >>> from generics import private

    >>> @private
    ... @attrs(frozen=True)
    ... class User:
    ...
    ...     def greet(self):
    ...         return 'Hello, Jeff'
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Define at least one encapsulated attribute

    ```

=== "dataclasses"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from generics import private

    >>> @private
    ... @dataclass(frozen=True)
    ... class User:
    ...
    ...     def greet(self):
    ...         return 'Hello, Jeff'
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Define at least one encapsulated attribute

    ```

=== "pydantic"

    ```pycon

    >>> from pydantic import BaseModel
    >>> from generics import private

    >>> @private
    ... class User(BaseModel):
    ...
    ...     def greet(self):
    ...         return 'Hello, Jeff'
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Define at least one encapsulated attribute

    ```

### Implementation inheritance is forbidden

First of all, there are two types of inheritance -
[subtyping inheritance](https://en.wikipedia.org/wiki/Subtyping) and
[implementation inheritance](<https://en.wikipedia.org/wiki/Inheritance_(object-oriented_programming)>).

It's nothing wrong with subtyping inheritance. It's used to create "is a"
relationship between classes. It's a technique where you can say that this class
is an implementation of this particular interface.
[`abc.Meta`](https://docs.python.org/3/library/abc.html) is one of the possible
approaches for implicit interface implementation in Python. It has alternatives
like [Duck typing](https://en.wikipedia.org/wiki/Duck_typing) and
[`typing_extensions.Protocol`](https://mypy.readthedocs.io/en/stable/protocols.html#simple-user-defined-protocols).
Yet again, it's nothing wrong with it if you want to design **contracts** in
your codebase using `abc.Meta`.

On the other hand, implementation inheritance was designed for
[code reuse](<https://en.wikipedia.org/wiki/Inheritance_(object-oriented_programming)#Code_reuse>)
in its heart. That's where things start to get out of hands. **Implementation
inheritance breaks encapsulation** by its definition. That's why it's easy to
end up with code like that:

```pycon

>>> from app import Entity

>>> class User(Entity):
...     database_table = 'users'
...     json_fields = ['id', 'name', 'surname', 'bio']
...     permissions = ['can_read', 'can_edit']
...     query_string_params = ['user_*']

```

Looking just at that code it's impossible to answer these simple yet important
questions:

1. What responsibilities it has? (What it do?)
2. How to use this class? (What public methods does it have?)

Everything is hidden from us in the base class. And it has its own base classes
as well. You get where it's going.

That's why we forbid implementation inheritance.

=== "attrs"

    ```pycon

    >>> from attr import attrs, attrib
    >>> from generics import private

    >>> from app import Entity

    >>> @private
    ... @attrs(frozen=True)
    ... class User(Entity):
    ...     name = attrib()
    ...
    ...     def greet(self):
    ...         return f'Hello, {self.name}'
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Do not use inheritance (use composition instead)

    ```

=== "dataclasses"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from generics import private

    >>> from app import Entity

    >>> @private
    ... @dataclass(frozen=True)
    ... class User(Entity):
    ...     name: str
    ...
    ...     def greet(self):
    ...         return f'Hello, {self.name}'
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Do not use inheritance (use composition instead)

    ```

=== "pydantic"

    ```pycon

    >>> from pydantic import BaseModel
    >>> from generics import private

    >>> from app import Entity

    >>> @private
    ... class User(Entity, BaseModel):
    ...     name: str
    ...
    ...     class Config:
    ...         allow_mutation = False
    ...
    ...     def greet(self):
    ...         return f'Hello, {self.name}'
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Do not use inheritance (use composition instead)

    ```

!!! note

    Subtyping inheritance with `abc.Meta` is not implemented yet.  We have plans to implement it in the future.

### Underscore names are forbidden

As we mentioned at the beginning of the document, Python has a convention for
private attributes and methods to start with a single underscore (`_`)
character. This harms readability. Thus they are forbidden. The library hides
everything properly anyway.

The presence of private methods especially is a sign of bad design. That means
that the class has too many layers of abstractions hidden in it. The intention
to hide methods defined in the class means that they operate on a lower level of
abstractions that the responsibility of the class belongs to. Instead of using
the composition of objects and encapsulation, the author decides to use uglier
names. That gives hope to the author that users will not use methods with ugly
names in their code. A bad design indeed.

=== "attrs"

    ```pycon

    >>> from attr import attrs, attrib
    >>> from generics import private

    >>> @private
    ... @attrs(frozen=True)
    ... class User:
    ...     _name = attrib()
    ...     surname = attrib()
    ...
    ...     def greet(self):
    ...         return f'Hello, {self._name} {self.surname}'
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Do not use private attributes

    ```

=== "dataclasses"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from generics import private

    >>> @private
    ... @dataclass(frozen=True)
    ... class User:
    ...     _name: str
    ...     surname: str
    ...
    ...     def greet(self):
    ...         return f'Hello, {self._name} {self.surname}'
    Traceback (most recent call last):
      ...
    _generics.exceptions.GenericClassError: Do not use private attributes

    ```

!!! note

    This check is not supported if you are using `pydantic` library due to its limitations.

### Prefer immutable classes

Awoid changing inner state of the classes as much as possible.

Way too many problems was caused because of changed data in unexpected parts of
code. To deal with such problem we should respect transparency of the
references. **Always create new name for the new state**.

Instead of protecting different parts of the code with same conditional
statements, make methods of a class return a new instance of the class if it
need to change something.

_Bad_:

=== "attrs"

    ```pycon

    >>> from attr import attrs, attrib
    >>> from generics import private

    >>> @private
    ... @attrs
    ... class User:
    ...     name = attrib()
    ...
    ...     def rename(self, name):
    ...         self.name = name

    >>> User(name='Jeff').rename('John')

    ```

=== "dataclasses"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from generics import private

    >>> @private
    ... @dataclass
    ... class User:
    ...     name: str
    ...
    ...     def rename(self, name):
    ...         self.name = name

    >>> User(name='Jeff').rename('John')

    ```

=== "pydantic"

    ```pycon

    >>> from pydantic import BaseModel
    >>> from generics import private

    >>> @private
    ... class User(BaseModel):
    ...     name: str
    ...
    ...     def rename(self, name):
    ...         self.name = name

    >>> User(name='Jeff').rename('John')

    ```

_Good_:

=== "attrs"

    ```pycon

    >>> from attr import attrs, attrib, evolve
    >>> from generics import private

    >>> @private
    ... @attrs
    ... class User:
    ...     name = attrib()
    ...
    ...     def rename(self, name):
    ...         return evolve(self, name=name)

    >>> User(name='Jeff').rename('John')
    User(name='John')

    ```

=== "dataclasses"

    ```pycon

    >>> from dataclasses import dataclass, replace
    >>> from generics import private

    >>> @private
    ... @dataclass
    ... class User:
    ...     name: str
    ...
    ...     def rename(self, name):
    ...         return replace(self, name=name)

    >>> User(name='Jeff').rename('John')
    User(name='John')

    ```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The generics library is part of the SOLID python family.</i></p>
