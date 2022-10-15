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
...         return f"Hello, {self._name}"

>>> user = User("Jeff")

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
- [Class methods are forbidden](#class-methods-are-forbidden)
- [Instance methods can return instances](#instance-methods-can-return-instances)
- [Instance methods can not be called on classes](#instance-methods-can-not-be-called-on-classes)
- [At least one instance method is required](#at-least-one-instance-method-is-required)
- [At least one encapsulated attribute is required](#at-least-one-encapsulated-attribute-is-required)
- [Variable-length encapsulated attributes are forbidden](#variable-length-encapsulated-attributes-are-forbidden)
- [Keyword encapsulated attributes are forbidden](#keyword-encapsulated-attributes-are-forbidden)
- [Implementation inheritance is forbidden](#implementation-inheritance-is-forbidden)
- [Underscore names are forbidden](#underscore-names-are-forbidden)
- [Class attributes are forbidden](#class-attributes-are-forbidden)
- [Prefer immutable classes](#prefer-immutable-classes)
- [Methods would have representation](#methods-would-have-representation)

### All methods are public

The main purpose of objects in object-oriented programming is in **behavior**
they could provide to the client code.

Behavior intended by object could be expressed with its methods.

Thus every instance and class method of the object is public. Class should be
decorated with `@private` function.

```pycon

>>> from generics import private

>>> @private
... class User:
...     def __init__(self, name):
...         self.name = name
...
...     def __repr__(self):
...         return f"User({self.name=!r})"
...
...     def greet(self):
...         return f'Hello, {self.name}'

>>> User
Private::User

>>> user = User('Jeff')
>>> user
Private::User(self.name='Jeff')

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
AttributeError: 'Private::User' object has no attribute 'name'

```

### Static methods are forbidden

Good objects expose their behavior and hide their state. The behavior objects
expose should be related to the state object hides. This metric is called
cohesion.

Static methods can't access the inner state of the object. That's why the
behavior they expose doesn't relate to the object. Cohesion will go down. That's
why we forbid static methods.

If you need such behavior, put it outside of the class. If this behavior is
necessary in the instance method of the original class, encapsulate it. Pass
that new thing to the constructor and access it in methods.

```pycon

>>> from generics import private

>>> @private
... class User:
...     def __init__(self, name):
...         self.name = name
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

### Class methods are forbidden

As we mentioned earlier, objects should expose behavior. Class methods do not
have access to any kind of inner state sinse there is no object encapsulating
it. That's why we forbid class methods.

```pycon

>>> from generics import private

>>> @private
... class User:
...     @classmethod
...     def create(cls):
...         pass
...
...     def __init__(self, name):
...         self.name = name
...
...     def greet(self):
...         return f'Hello, {self.name}'
Traceback (most recent call last):
  ...
_generics.exceptions.GenericClassError: Do not use class methods (call constructor instead)

```

### Instance methods can return instances

In case your object return another instance of the same class from its method,
this instance would be `@private` as well. This is a good practice to follow.
For example, instead of assigning new value to the attributes (aka setters),
create new instance of the class with necessary changes and return it from
method. Immutability is a powerful technique, which would help you to build safe
architecture suitable for multi-threaded applications.

See more in [Prefer immutable classes](#prefer-immutable-classes).

### Instance methods can not be called on classes

In some cases, it's technically possible to use instance methods as functions,
if you pass value of `self` directly as argument. This behavior is hacky. That's
why `generics` library forbid explicitly a call of instance methods using class
attribute access.

```pycon

>>> from generics import private

>>> @private
... class User:
...     def __init__(self, name):
...         self.name = name
...
...     def greet(self):
...         return 'Hello, anonymous'

>>> class AnotherUser:
...     name = 'Jeff'

>>> User.greet(AnotherUser())
Traceback (most recent call last):
  ...
_generics.exceptions.GenericClassError: Instance methods can not be called on classes

```

### At least one instance method is required

As we mention a couple of times earlier the main goal of the good objects is to
expose behavior. If there is no methods defined on the class, it's not possible
to expose any kind of behavior. The object becomes useless.

Class methods does not count since it has a different purpose.

```pycon

>>> from generics import private

>>> @private
... class User:
...     def __init__(self, name):
...         self.name = name
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

```pycon

>>> from generics import private

>>> @private
... class User:
...
...     def greet(self):
...         return 'Hello, Jeff'
Traceback (most recent call last):
  ...
_generics.exceptions.GenericClassError: Define at least one encapsulated attribute

```

!!! note

    `generics` library assumes that constructor of the decorated class will assign
    its arguments to the instance properties with same names. That's why encapsulated
    attributes are inferred from constructor arguments.

### Variable-length encapsulated attributes are forbidden

Classes should not encapsulate average set of attributes. This makes code hard
to reason about. This makes object state unrepresented in the source code.

```pycon

>>> from generics import private

>>> @private
... class User:
...
...     def __init__(self, *args):
...         self.args = args
...
...     def greet(self):
...         return 'Hello, Jeff'
Traceback (most recent call last):
  ...
_generics.exceptions.GenericClassError: Class could not have variable encapsulated attribute

```

### Keyword encapsulated attributes are forbidden

Classes should not encapsulate attributes which names defined outside of the
class. This makes code hard to reason about. This makes object structure
unrepresented in the source code.

```pycon

>>> from generics import private

>>> @private
... class User:
...
...     def __init__(self, **kwargs):
...         self.kwargs = kwargs
...
...     def greet(self):
...         return 'Hello, Jeff'
Traceback (most recent call last):
  ...
_generics.exceptions.GenericClassError: Class could not have keyword encapsulated attribute

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
If you want to design **contracts** in your codebase using `abc.Meta`, we advice
you not to do so. `Protocol` would make it possible to define contract close to
the place where object of this interface would be used. The most practical place
to put interface declaration. More importantly it would not create broken (from
the point of logic) import graph and would not force you to create dumb top-down
architecture. `abc.Meta` makes both of these goals hard to achieve.

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

```pycon

>>> from generics import private

>>> from app import Entity

>>> @private
... class User(Entity):
...     def __init__(self, name):
...         self.name = name
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

```pycon

>>> from generics import private

>>> @private
... class User:
...     def __init__(self, name, _surname):
...         self.name = name
...         self._surname = _surname
...
...     def greet(self):
...         return f'Hello, {self.name} {self._surname}'
Traceback (most recent call last):
  ...
_generics.exceptions.GenericClassError: Do not use private attributes

```

### Class attributes are forbidden

If you keep in mind that classes decorated with `@private` decorator does not
expose instance attributes, you would agree that class attributes in that case
became useless.

Usually, it would be used as some kind of marker for external purposes. Let say
some kind of regestry could access class attribute to make decision what to do
with class.

_Bad_:

```pycon

>>> class User:
...     bot_flag = False

>>> def register(cls):
...     if cls.bot_flag:
...         print('extend bot registry')

>>> register(User)

```

_Good_:

```pycon

>>> from generics import private

>>> @private
... class User:
...     def __init__(self, name):
...         self.name = name
...
...     def is_bot(self):
...         return False

>>> def register(visitor):
...     if visitor.is_bot():
...         print('extend bot registry')

>>> register(User('Jeff'))

```

In some cases people tend to use class attributes as some kind of constants to
be used by methods of the class. Most common intent for such style would be
abbility to override that constant using inheritance. We consider this practice
an antipattern as well. Our suggestion would be to move this constant to the
default value of the keyword argument of the method.

If you need this constant in more than one method of your class, it is a clear
sign that your class is doing too much. It's a code smell related to the
[Single-responsibility principle](https://en.wikipedia.org/wiki/Single-responsibility_principle).
Do not define module level uppercase-named variable. Do not repeat same keyword
argument in many methods of the same class. Instead of this you could extract
logic related to the constant into a smaller low-level class. After that you
would be able to encapsulate its instance into original class and remove existed
duplication.

_Bad_:

```pycon

>>> class User:
...     active_status = 'active'
...
...     def __init__(self, status):
...         self.status = status
...
...     def is_active(self):
...         return self.status == self.active_status

>>> user = User('banned')
>>> user.is_active()
False

```

_Good_:

```pycon

>>> from generics import private

>>> @private
... class User:
...     def __init__(self, status):
...         self.status = status
...
...     def is_active(self, active_status='active'):
...         return self.status == active_status

>>> user = User('banned')
>>> user.is_active()
False

```

Which that reasons in mind `generics` library deny class attributes to be
defined on classes decorated with `@private` decorator.

```pycon

>>> from generics import private

>>> @private
... class User:
...     alive = True
...
...     def __init__(self, name):
...         self.name = name
...
...     def greet(self):
...         return f'Hello, {self.name}'
Traceback (most recent call last):
  ...
_generics.exceptions.GenericClassError: Do not define attributes on classes

```

### Prefer immutable classes

Awoid changing inner state of the classes as much as possible.

Way too many problems was caused because of changed data in unexpected parts of
code. To deal with such problem we should respect transparency of the
references. **Always create new name for the new state**.

Instead of protecting different parts of the code with same conditional
statements, make methods of a class return a new instance of the class if it
need to change something.

_Bad_:

```pycon

>>> from generics import private

>>> @private
... class User:
...     def __init__(self, name):
...         self.name = name
...
...     def rename(self, name):
...         self.name = name

>>> User(name='Jeff').rename('John')

```

_Good_:

```pycon

>>> from generics import private

>>> @private
... class User:
...     def __init__(self, name):
...         self.name = name
...
...     def __repr__(self):
...         return f"User({self.name=!r})"
...
...     def rename(self, name):
...         return User(name)

>>> User(name='Jeff').rename('John')
Private::User(self.name='John')

```

### Methods would have representation

In some cases, instead of object composition people would create composition of
callables. Usually, this happens when you pass bound method of one object into
constructor of another object. Service objects tend to do this a lot. Most of
the time they primary goal to trigger some action. Such objects are rarely
interested in knowledge who would implement the action. To make service objects
representation look nice, generics library provides representation to class and
instance methods of `@private` classes.

```pycon

>>> @private
... class Registration:
...     def __init__(self, send_message):
...         self.send_message = send_message
...
...     def __repr__(self):
...         return f"Registration(\n    {self.send_message=!r}\n)"
...
...     def sign_up(self, phone):
...         self.send_message(phone)

>>> @private
... class Message:
...     def __init__(self, text):
...         self.text = text
...
...     def __repr__(self):
...         return f"SignUp({self.text=!r})"
...
...     def send(self, phone):
...         print(f"Message {self.text!r} was sent to {phone!r}")

>>> message = Message("Welcome to the service")

>>> registration = Registration(message.send)

>>> registration.sign_up("911")
Message 'Welcome to the service' was sent to '911'

>>> registration
Private::Registration(
    self.send_message=Private::SignUp(self.text='Welcome to the service').send
)

```

<p align="center">&mdash; ⭐ &mdash;</p>
