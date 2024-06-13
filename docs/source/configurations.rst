.. _config-label:

Configurations
==============

Precedence
----------

Csort configurations follow a hierarchical design pattern.

1. Command line configurations - see :ref:`cli-custom-config-label`

2. Configuration files - ``pyproject.toml`` / ``csort.ini``

3. Default configurations

The recommended pattern is to use a ``pyproject.toml`` file.

Defaults
--------

Csort configurations can be split into **ordering** and **general**.

General defaults
................
:auto_static: Defaults to True

Check to see if methods could be static methods and convert to a static method if so.

:use_csort_group: Defaults to True

Controls whether the ``csort_group`` decorator should be considered when running csort. See :ref:`csort-group-label`

Ordering defaults
.................

See :ref:`components-label` for details on each component.

:ellipsis: Defaults to 0
:class docstring: Defaults to 0
:typed class attribute: Defaults to 1
:untyped class attribute: Defaults to 2
:dunder methd: Defaults to 3
:csort group: Defaults to 4
:class method: Defaults to 5
:static method: Defaults to 6
:property: Defaults to 7
:getter: Defaults to 8
:setter: Defaults to 9
:deleter: Defaults to 10
:decorated method: Defaults to 11
:instance method: Defaults to 12
:private method: Defaults to 13
:inner class: Defaults to 14

Configuration Files
-------------------

Configurations can be specified using the legacy ``csort.ini`` file or the more modern ``pyproject.toml``
file.

By default, csort will search for a configuration file named either ``csort.ini`` or ``pyproject.toml`` in the
working directory.

An alternatively named ``.ini`` or ``.toml`` file can also be used and then specified to csort using the
``--config-path`` option on the command line.

pyproject.toml
..............
Below is an example ``pyproject.toml`` with csort tool groups

.. code-block:: toml

    [tool.csort.order]
    dunder_method = 3
    csort_group = 4
    class_method = 5
    static_method = 6
    getter = 7
    setter = 8
    property = 9
    decorated_method = 10
    instance_method = 11
    private_method = 12
    inner_class = 13

    [tool.csort]
    use_csort_group = true
    auto_static = false

In this example configuration, ``property`` methods have been set to level 9, below ``getter`` and ``setter``.
By default, ``property`` is normally level 7.


csort.ini
.........

Below is an example ``csort.ini`` file

.. code-block:: ini

    [csort.order]
    dunder_method = 3
    private_method = 4
    csort_group = 5
    class_method = 6
    static_method = 7
    property = 8
    getter = 9
    setter = 10
    deleter = 11
    decorated_method = 12
    instance_method = 13
    inner_class = 14

    [csort]
    use_csort_group = True
    auto_static = False

In this example configuration, ``private_method`` has been set to level 4 so that
private methods appear at the top of the class rather than the bottom.
