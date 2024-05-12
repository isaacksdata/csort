# Csort

Formatter for automatic re-ordering of methods defined within classes.

## Usage

Csort is a command line tool which can be run using:

```commandline
csort --input-path src/my_python_script.py
```

If an output path is not specified, then Csort will modify the original source code file. To write to a new file:

```commandline
csort --input-path src/my_python_script.py --output-path src/my_output_scripy.py
```

Csort can run recursively over `.py` files by specifying a directory as the input path:

```commandline
csort --input-path src/
```

Csort can put all the outputs after formatting a directory of `.py` scripts into a new output directory:

```commandline
csort --input-path src/my_python_script.py --output-path src/csorted/
```

Csort can be run selectively by specifying skip patterns to exclude files with those patterns in the file name:

```commandline
csort --input-path src/ -sp exclude_1 -sp exclude_2
```

Csort can be run in `check` mode. No files will be modified and Csort will report the number of files which would be
modified:

```commandline
csort --input-path src/ --check
```

Csort can be run in `diff` mode. No files will be modified and Csort will report the class method order changes for
each class in each `.py` script:

```commandline
csort --input-path src/ --diff
```

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

- logging level cli option
- move to libcst from ast
- Check that pandas querys are preserved e.g. "'column' == 'mystring'"
- use pyproject.toml instead of setup files
- support pyproject.toml
- auto convert to static method
- pre-commit hook
- pypy
- tox
- sphinx documentation
