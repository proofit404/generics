# Installation

The generics library is available on PyPI.

To install it run:

```bash
pip install -U generics
```

We use [semantic release](https://semantic-release.gitbook.io/semantic-release/)
to publish packages as soon as pull requests land to the master branch. It's not
necessary to use develompment version of the library.

We officially support three last minor releases of CPython interpreter and last
minor release of PyPy interpreter. We highly recommend the latest patch release
of each Python series.

## Third-party libraries

If you want to use `pydantic` models as private classes, you could consider to
use `pydantic-initialized` library as compatibility layer for that purpose.

```bash
pip install -U pydantic-initialized
```

<p align="center">&mdash; ⭐️ &mdash;</p>
<p align="center"><i>The generics library is part of the SOLID python family.</i></p>
