# Dependencies

It is possible to instantiate classes decorated with `@private` function via
[dependencies](https://proofit404.github.io/dependencies/) library.

=== "attrs"

    ```pycon

    >>> from attr import attrs, attrib
    >>> from dependencies import Injector
    >>> from generics import private

    >>> @private
    ... @attrs(frozen=True)
    ... class User:
    ...     name = attrib()
    ...
    ...     def greet(self):
    ...         return f'Hello, {self.name}'

    >>> class UserContainer(Injector):
    ...     user = User
    ...     name = 'Jeff'

    >>> UserContainer.user.greet()
    'Hello, Jeff'

    ```

=== "dataclasses"

    ```pycon

    >>> from dataclasses import dataclass
    >>> from dependencies import Injector
    >>> from generics import private

    >>> @private
    ... @dataclass(frozen=True)
    ... class User:
    ...     name: str
    ...
    ...     def greet(self):
    ...         return f'Hello, {self.name}'

    >>> class UserContainer(Injector):
    ...     user = User
    ...     name = 'Jeff'

    >>> UserContainer.user.greet()
    'Hello, Jeff'

    ```
