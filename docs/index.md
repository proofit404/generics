# Generics

[![azure-devops-builds](https://img.shields.io/azure-devops/build/proofit404/generics/4?style=flat-square)](https://dev.azure.com/proofit404/generics/_build/latest?definitionId=4&branchName=master)
[![azure-devops-coverage](https://img.shields.io/azure-devops/coverage/proofit404/generics/4?style=flat-square)](https://dev.azure.com/proofit404/generics/_build/latest?definitionId=4&branchName=master)
[![pypi](https://img.shields.io/pypi/v/generics?style=flat-square)](https://pypi.python.org/pypi/generics/)

A classy toolkit designed with OOP in mind.

**[Documentation](https://proofit404.github.io/generics/) | [Source Code](https://github.com/proofit404/generics) | [Task Tracker](https://github.com/proofit404/generics/issues)**

In our opinion, main benefits of having objects implemented in the
language are encapsulation and polymorphous. Classes that could be
easily used in a composition are tricky to write. The `generics`
library aims to help you in writing code with high quality.

## Pros

- Real private attributes without loosing the readability
- Leads to a better design forcing you to use encapsulation properly
- Makes writing quality code with high cohesion and low coupling easier
- Guides you to follow SOLID principles

## Example

The `generics` library gives you an easy way to define private
attributes on objects without loosing little nice things like
readability.

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

>>> user = User('Jeff')

>>> user.greet()
'Hello, Jeff'

>>> hasattr(user, 'name')
False

```

## Questions

If you have any questions, feel free to create an issue in our [Task Tracker](https://github.com/proofit404/generics/issues). We have the [question label](https://github.com/proofit404/generics/issues?q=is%3Aopen+is%3Aissue+label%3Aquestion) exactly for this purpose.

## License

Generics library is offered under the two clause BSD license.

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The generics library is part of the SOLID python family.</i></p>