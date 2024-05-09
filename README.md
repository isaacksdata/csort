# Csort

Formatter for automatic re-ordering of methods defined within classes.

## Summary

Csort is a formatter for python classes. Currently, there is no prescribed convention for how the methods of a class
should be organised. There are some expectations, such as dunder methods being at the top of the class but this is
generally not enforced.

Csort aims to be a formatter along the lines of `black` and `isort` which can be used to reorder the methods of a class
according to some pre-described ordering pattern.

By default, Csort orders in the following way:

1. Type annotated attributes - e.g. `self.name: str = "MyClass"`
1. Unannotated attributes - e.g. `self.name = "MyClass"`
1. Dunder methods - e.g. `__init__`
1. Class methods - `@classmethod`
1. Static methods - `@staticmethod`
1. Properties - `@property`
1. Getters - `@name.getter`
1. Setters - `@name.setter`
1. Other decorated methods - sorted by decorator alphabetically - e.g. `@lru_cache`, `@abstractmethod`
1. Instance methods - `def func(self): pass`
1. Private methods - `def _func(self): pass`

If multiple methods occur for a given sorting level, then the methods are sorted alphabetically.

## Todo

- use pyproject.toml instead of setup files
- support pyproject.toml
- auto convert to static method
- pre-commit hook
- pypy
- tox
- sphinx documentation
