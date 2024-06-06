Usage
=====

Installation
------------

To use csort, first install it using pip:

.. code-block:: console

   $ pip install csort

Alternatively, use csort as a **pre-commit** hook - :ref:`precommit-label`.


Command Line Usage
------------------
This section documents csort's command line interface.

Input code
..........

You can specify which python files should be checked by passing in the paths:

.. code-block:: console

    $ csort foo.py bar.py

The code to be checked can be supplied in a couple of other ways:

.. option:: -ip INPUT-PATH, --input-path INPUT-PATH

    If the input path is a ``.py`` file then only that code will be checked.
    If the input path is a directory or module, then csort will recursively check all code under
    the path.

.. option:: -sp SKIP-PATTERNS --skip-patterns SKIP-PATTERNS

    Use the ``--skip-patterns`` option to indicate exclusion criteria. If the supplied pattern is found in a ``.py``
    then it will not be checked. To supply multiple patterns, use the option multiple times.

    $ csort --sp pat1 --sp pat2

Output code
...........

By default, csort will modify the original code but this behaviour can be modified using the ``--output-path`` option:

.. option:: -o OUTPUT-PATH, --output-path OUTPUT-PATH

    If the output path and input path are singular ``.py`` file then only that code will be checked and the modified
    code will be written to the supplied output path, creating a new file if needed.
    If the output path is a directory, then the modified code will be saved to a ``.py`` file with the same name as the
    input but in the newly created output directory.
    If the output path is a single ``.py`` file but the input path is a directory, then an exception will be raised.

Custom configurations
.....................

Default configurations regarding the preferred order of methods is built into csort.

The defaults can be overridden by using a configuration file - see :ref:`config-label`.

If the configuration file has a non-standard name (i.e. not ``csort.ini`` or ``pyproject.toml``) then the path can be
specified using the ``--config-path`` option.

.. option:: -cp CONFIG-PATH, --config-path CONFIG-PATH

    This should be the relative path to a ``.ini`` or ``.toml`` file from which csort configurations can be loaded.

Alternative modes
.................

Csort can be executed in alternative modes which do not modify the code.

.. option:: --check CHECK

    Runs csort and reports on the number of files which would be modified.

.. option:: --diff DIFF

    Runs csort and reports on the differences which would be made.


Misc
....

.. option:: -v VERBOSE, --verbose VERBOSE

    Modify the logging level of csort.
    0 - no logging output
    1 - warnings and info
    2 - debug level


.. option:: -p PARSER, --parser PARSER

    Specify whether to use the AST or CST code parser. Defaults to CST parser and this is recommended.

    See :ref:`parsing-label` for more details.


Import Usage
------------
