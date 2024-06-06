.. Csort documentation master file, created by
   sphinx-quickstart on Thu Jun  6 20:02:03 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Csort's documentation!
=================================

**Csort** is a python library for formatting python classes.

Csort can keep components of classes in a pre-defined order according to method names and decorators.

This can be useful for navigating complex classes, maintaining readability and, through the ``csort_group`` decorator,
grouping directly related methods together.

Here is an example python class with three methods:

* ``__init__()``
* ``func()``
* ``_private_func()``

.. code-block:: python

 class ExampleClass:

   def _private_func(self):
      print("This is a private method!")

   def __init__(self):
      self.name: str = "example"

   def func(self):
      print("This is your average method!")


Running **csort** with default configurations would carry out two key changes to ``ExampleClass``.

First, the methods would be re-ordered such that **dunder** methods come first, followed by the average method,
``func``, followed by the private method ``_private_func``.

Second, csort can automatically detect methods which could be made into a **static method**.

The result would be:

.. code-block:: python

 class ExampleClass:

   def __init__(self):
      self.name: str = "example"

   @staticmethod
   def func():
      print("This is your average method!")

   @staticmethod
   def _private_func():
      print("This is a private method!")


Contents
--------

.. toctree::

   usage
   pre_commit
   parsing
   components
   configurations



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
