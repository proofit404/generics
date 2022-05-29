# Generics [![build](https://img.shields.io/github/workflow/status/proofit404/generics/release?style=flat-square)](https://github.com/proofit404/generics/actions/workflows/release.yml?query=branch%3Arelease) [![pypi](https://img.shields.io/pypi/v/generics?style=flat-square)](https://pypi.org/project/generics)

A classy toolkit designed with OOP in mind.

**[Documentation](https://proofit404.github.io/generics) |
[Source Code](https://github.com/proofit404/generics) |
[Task Tracker](https://github.com/proofit404/generics/issues)**

In our opinion, main benefits of having objects implemented in the language are
encapsulation and polymorphous. Classes that could be easily used in a
composition are tricky to write. The `generics` library aims to help you in
writing code with high quality.

## Pros

- Real private attributes without loosing the readability
- Leads to a better design forcing you to use encapsulation properly
- Makes writing quality code with high cohesion and low coupling easier
- Guides you to follow SOLID principles

## Example

The `generics` library gives you an easy way to define private attributes on
objects without loosing little nice things like readability.

```pycon

>>> from generics import private

>>> @private
... class User:
...     def __init__(self, name):
...         self.name = name
...
...     def greet(self):
...         return f"Hello, {self.name}"

>>> user = User("Jeff")

>>> user.greet()
'Hello, Jeff'

>>> hasattr(user, "name")
False

```

## Questions

If you have any questions, feel free to create an issue in our
[Task Tracker](https://github.com/proofit404/generics/issues). We have the
[question label](https://github.com/proofit404/generics/issues?q=is%3Aopen+is%3Aissue+label%3Aquestion)
exactly for this purpose.

## Enterprise support

If you have an issue with any version of the library, you can apply for a paid
enterprise support contract. This will guarantee you that no breaking changes
will happen to you. No matter how old version you're using at the moment. All
necessary features and bug fixes will be backported in a way that serves your
needs.

Please contact [proofit404@gmail.com](mailto:proofit404@gmail.com) if you're
interested in it.

## License

`generics` library is offered under the two clause BSD license.

<p align="center">&mdash; ⭐ &mdash;</p>
