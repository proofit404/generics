# 5.0.0 (2022-10-15)

### Features

- deny class methods on [@private](https://github.com/private) classes
  [#238](https://github.com/proofit404/generics/issues/238) 2be2561

### BREAKING CHANGES

- It is used to instantiate classes. We use `dependencies` library and stories
  state normalization for such things. I would like not to work on same thing
  twice. In addition I personally would never use factory method pattern. The
  worst part, it broke `@delegated` decorator semantic since it planned to be
  used with instances only. Class methods on delegated classes does not make
  sense.

# 4.0.0 (2022-10-14)

### Code Refactoring

- drop abc.Meta subtyping
  [#57](https://github.com/proofit404/generics/issues/57) 1ea34e5

### Features

- deny class attributes [#57](https://github.com/proofit404/generics/issues/57)
  ee512f7

### BREAKING CHANGES

- Inheritance of any kind is not allowed any more. If you are using `abc.Meta`,
  we suggest to use `typing.Protocol` instead.

# 3.9.0 (2022-07-24)

### Features

- deny keyword arguments in constructor
  [#213](https://github.com/proofit404/generics/issues/213) 5d0c4e1

# 3.8.0 (2022-07-14)

### Features

- protect instances returned from methods
  [#233](https://github.com/proofit404/generics/issues/233) 20d1703

# 3.7.0 (2022-07-14)

### Features

- implement methods representation
  [#231](https://github.com/proofit404/generics/issues/231) 67927ce

# 3.6.0 (2022-07-13)

### Features

- implement [@delegated](https://github.com/delegated) decorator
  [#77](https://github.com/proofit404/generics/issues/77) 916fd1f

# 3.5.0 (2022-05-28)

### Features

- protect from star args constructor
  [#212](https://github.com/proofit404/generics/issues/212) 656d370

# 3.4.0 (2021-08-18)

### Features

- allow inheritance from interface
  [#94](https://github.com/proofit404/generics/issues/94)

## 3.3.1 (2021-04-07)

### Bug Fixes

- ignore dunder class methods
  [#223](https://github.com/proofit404/generics/issues/223)

# 3.3.0 (2021-02-17)

### Features

- deny to call class methods on instances
  [#220](https://github.com/proofit404/generics/issues/220)

## 3.2.1 (2021-01-08)

### Bug Fixes

- allow private methods defined globally
  [#215](https://github.com/proofit404/generics/issues/215)

# 3.2.0 (2021-01-06)

### Features

- rewrite without third-party libraries
  [#200](https://github.com/proofit404/generics/issues/200)

# 3.1.0 (2020-11-20)

### Features

- support pypy interpreter [#9](https://github.com/proofit404/generics/issues/9)

# 3.0.0 (2020-11-12)

### Build System

- add python 3.9 support
  [#186](https://github.com/proofit404/generics/issues/186)

### BREAKING CHANGES

- drop python 3.6 support.

# 2.0.0 (2020-08-30)

### Code Refactoring

- drop Python 2.7 and 3.4 support
  [#134](https://github.com/proofit404/generics/issues/134)

### BREAKING CHANGES

- Due to the our new policy of enterprise user support we will drop abandoned
  version of python and libraries we are integrated with as soon as they reach
  official end of life.

# 1.1.0 (2020-08-21)

### Features

- support dependencies library

## 1.0.1 (2020-08-06)

### Bug Fixes

- fake [@defended](https://github.com/defended) and
  [@delegated](https://github.com/delegated) decorators

# 1.0.0 (2020-07-03)

### Features

- implement `@private` decorator

<p align="center">&mdash; ⭐ &mdash;</p>
