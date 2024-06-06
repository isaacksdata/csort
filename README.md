<a href="https://github.com/isaacksdata/csort/actions/workflows/test_publish.yaml"><img src="https://github.com/isaacksdata/csort/actions/workflows/test_publish.yaml/badge.svg"></a>
<a href="https://github.com/isaacksdata/csort/actions/workflows/tox_ci.yaml"><img src="https://github.com/isaacksdata/csort/actions/workflows/tox_ci.yaml/badge.svg"></a>
<a href="https://codecov.io/gh/isaacksdata/csort"><img src="https://codecov.io/gh/isaacksdata/csort/branch/main/graph/badge.svg"></a>
![PyPI Version](https://img.shields.io/pypi/v/csort.svg)
![Python versions](https://img.shields.io/badge/Python-3.9--3.12-blue.svg)
<a href="https://github.com/isaacksdata/csort/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit" alt="pre-commit" style="max-width:100%;"></a>
<a href="https://mypy-lang.org/"><img src="https://www.mypy-lang.org/static/mypy_badge.svg"></a>
<a href="https://tox.wiki/en/4.15.0/"><img alt="using: tox" src="https://img.shields.io/badge/using-tox-00AA00.svg"></a>
<a href="https://pylint.readthedocs.io/en/stable/"><img alt="using: pylint" src="https://img.shields.io/badge/pylint-10.0-blue.svg"></a>

# Csort

Formatter for automatic re-ordering of methods defined within classes.

## Install

Install from `testpypi` using:

```commandline
pip install -i https://test.pypi.org/pypi/ --extra-index-url https://pypi.org/simple csort
```

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

Csort can be run using Abstract Syntax Tree (AST) or Concrete Syntax Tree (CST) parsers. The AST parser is simpler
but does always preserve code format such as line spacing, comments and quoting style. Csort handles some of these
inconsistencies such as line spacing and comments by borrowing parsing information from `ast_comments` and `astor`.
However, quoting style is not guaranteed with the AST parser. The CST parser uses the `libcst` package and faithfully
preserves code style. It is recommended to use the CST parser with Csort and this is the default behaviour.
The parser can be specified using `--parser` or `-p` flags.

```commandline
csort --input-path src/ --parser cst
```

```commandline
csort --input-path src/ -p ast
```

Python classes can have methods which do not access or change the state of the instance. It can be useful to indicate
that a method does not affect the state by using the `@staticmethod` decorator and removing `self` from the
arguments of the method. Csort can automatically decorate methods which could be static with the `@staticmethod`
decorator. This behaviour can be controlled using the `auto_static` parameter in the `csort` section of the
`csort.ini` file. Alternatively, use the `--auto-static` flag on the command line to force the modifications, or use
`--n-auto-static` to block any static modifications. Note that the command line arguments take precedence over the
`csort.ini` parameters.

Auto convert to static methods:

```commandline
csort --input-path src/ --auto-static
```

Block conversion to static methods:

```commandline
csort --input-path src/ --n-auto-static
```

Csort configurations can be specified in either a `csort.ini` file or a `pyproject.toml` file. If both files are
present then the `pyproject.toml` file will take precedent.

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

## Pre-commit hook

Csort can be used with pre-commit to reformat python classes as part of CICD pipelines.

#### Steps:

Create a `.pre-commit-config.yaml` file in your project root

There are two options:

Option One - use a local installation of Csort

```yaml
  - repo: local
    hooks:
      - id: csort
        name: csort
        entry: csort
        language: system
        types: [python]
        args: []
```

Option Two - use the remote hook

```yaml
  - repo: https://github.com/isaacksdata/csort
    rev: v0.1.8
    hooks:
      - id: csort
        args: []
```

## Todo

- sphinx documentation
