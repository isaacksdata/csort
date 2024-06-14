Usage
=====

Installation
------------

To use msort, first install it using pip:

.. code-block:: console

   $ pip install msort

Alternatively, use msort as a **pre-commit** hook - :ref:`precommit-label`.


Command Line Usage
------------------
This section documents msort's command line interface.

Input code
..........

You can specify which python files should be checked by passing in the paths:

.. code-block:: console

    $ msort foo.py bar.py

The code to be checked can be supplied in a couple of other ways:

.. option:: -ip INPUT-PATH, --input-path INPUT-PATH

    If the input path is a ``.py`` file then only that code will be checked.
    If the input path is a directory or module, then msort will recursively check all code under
    the path.

.. option:: -sp SKIP-PATTERNS --skip-patterns SKIP-PATTERNS

    Use the ``--skip-patterns`` option to indicate exclusion criteria. If the supplied pattern is found in a ``.py``
    then it will not be checked. To supply multiple patterns, use the option multiple times.

    $ msort --sp pat1 --sp pat2

Output code
...........

By default, msort will modify the original code but this behaviour can be modified using the ``--output-path`` option:

.. option:: -o OUTPUT-PATH, --output-path OUTPUT-PATH

    If the output path and input path are singular ``.py`` file then only that code will be checked and the modified
    code will be written to the supplied output path, creating a new file if needed.
    If the output path is a directory, then the modified code will be saved to a ``.py`` file with the same name as the
    input but in the newly created output directory.
    If the output path is a single ``.py`` file but the input path is a directory, then an exception will be raised.

.. _cli-custom-config-label:

Custom configurations
.....................

Default configurations regarding the preferred order of methods is built into msort.

The defaults can be overridden by using a configuration file - see :ref:`config-label`.

If the configuration file has a non-standard name (i.e. not ``msort.ini`` or ``pyproject.toml``) then the path can be
specified using the ``--config-path`` option.

.. option:: -cp CONFIG-PATH, --config-path CONFIG-PATH

    This should be the relative path to a ``.ini`` or ``.toml`` file from which msort configurations can be loaded.

Csort configurations can also be overridden on the command line. Any field defined in the configuration file can be
re-defined on the command line.

Class component ordering preferences can set on the command line - :ref:`components-label` :

.. code-block:: console

   $ msort file.py --private-method=3 --dunder-method=12

This snippet would swap the default ordering of dunder methods and private methods.

Note, if you set multiple components to have the same sorting level then they will be sorted alphabetically.

Non-sorting parameters which are normally set in the configuration file can also be set on the command line.

.. option:: --auto-static AUTO-STATIC

    Check if a method could be made static and convert it if so (Default).

.. option:: --n-auto-static N-AUTO-STATIC

    Do not check for possible static methods.

.. option:: --use-msort-group USE-MSORT-GROUP

    Account for the ``msort_group()`` decorator during method sorting (Default). See :ref:`msort-group-label`.

.. option:: --n-use-msort-group N-USE-MSORT-GROUP

    Do not account for the ``msort_group()`` decorator during method sorting.

.. option:: --use-property-groups USE-PROPERTY-GROUPS

    Group methods related to a class property together.

.. option:: --n-use-property-groups N-USE-PROPERTY-GROUPS

    Do not group methods related to a class property together (Default).

Alternative modes
.................

Csort can be executed in alternative modes which do not modify the code.

.. option:: --check CHECK

    Runs msort and reports on the number of files which would be modified.

.. option:: --diff DIFF

    Runs msort and reports on the differences which would be made.


Misc
....

.. option:: -v VERBOSE, --verbose VERBOSE

    Modify the logging level of msort.
    0 - no logging output
    1 - warnings and info
    2 - debug level


.. option:: -p PARSER, --parser PARSER

    Specify whether to use the AST or CST code parser. Defaults to CST parser and this is recommended.

    See :ref:`parsing-label` for more details.


.. option:: -f FORCE, --force FORCE

    Force msort to allow manual override of sorting levels such that :ref:`methods-label` can be sorted with
    higher precedence than :ref:`fixed-components-label`.

.. _msort-group-label:

Import Usage
------------
Csort introduces the ``msort_group`` decorator which can be used to force a group of methods to be placed together
by msort.

This decorator can be useful if you have a complex class with subsets of related methods.

Lets work through an example:

.. code-block:: python

 class Dog:
    def __init__(self, name: str, color: str, owner: str) -> None:
        self.name = name
        self.color = color
        self.owner = owner

    @msort_group(group="movement")
    def run(self) -> None:
        print("The dog is running!")

    @staticmethod
    @msort_group(group="sound")
    def whimper() -> None:
        print("The dog is whimpering!")

    @msort_group(group="sound")
    def growling(self) -> None:
        print("The dog is growling!")

    @msort_group(group="movement")
    def walk(self) -> None:
        print("The dog is walking!")

    @msort_group(group="movement")
    def wag(self) -> None:
        print("The dog is wagging its tail!")

    @msort_group(group="sound")
    def bark(self) -> None:
        print("The dog is barking!")

    @msort_group(group="describe")
    def describe(self) -> None:
        print(f"The {self.color} dog called {self.name} is owned by {self.owner}")

    @msort_group(group="describe")
    def color_of_dog(self) -> None:
        print(f"The dog is {self.color}")

In this example, the ``Dog`` class uses the ``msort_group`` decorator to define three method groups: movement, sound
and describe.

Csort will interpret the ``msort_group`` decorator and sort the methods by the group name, then by any additional
sorting parameter and then alphabetically by name.

.. code-block:: python

 class Dog:
    def __init__(self, name: str, color: str, owner: str) -> None:
        self.name = name
        self.color = color
        self.owner = owner

    @msort_group(group="describe")
    def color_of_dog(self) -> None:
        print(f"The dog is {self.color}")

    @msort_group(group="describe")
    def describe(self) -> None:
        print(f"The {self.color} dog called {self.name} is owned by {self.owner}")

    @msort_group(group="movement")
    def run(self) -> None:
        print("The dog is running!")

    @msort_group(group="movement")
    def wag(self) -> None:
        print("The dog is wagging its tail!")

    @msort_group(group="movement")
    def walk(self) -> None:
        print("The dog is walking!")

    @staticmethod
    @msort_group(group="sound")
    def whimper() -> None:
        print("The dog is whimpering!")

    @msort_group(group="sound")
    def bark(self) -> None:
        print("The dog is barking!")

    @msort_group(group="sound")
    def growling(self) -> None:
        print("The dog is growling!")

In the msort formatted ``Dog`` class, the methods are sorted by group with the describe group first, then the movement
group and finally the sound group. Also notice that sorting withing groups is alphabetical, except ``whimper()`` which
is the first sound group method as it also has the ``@staticmethod`` decorator, affording it a higher rank than the
other instance methods. See :ref:`components-label` for default ranks.
