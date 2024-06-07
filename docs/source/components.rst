.. _components-label:

Components
==========
Csort formats python classes by re-ordering the components of classes into a pre-defined order.

The first level of ordering depends on the type of component.

The second level of ordering depends on the name of the component.

Fixed components
----------------
There are currently four types of fixed components which cannot be manually overridden by the user.

Ellipsis
........
The ellipsis has multiple uses in python but for csort it can appear as a component when used as a
placeholder for a class which has not been implemented yet or during multi-inheritance patterns.

.. code-block:: python

 class NotImplementedClass:
    ...

.. code-block:: python

 class ConcreteClass(ParentClassOne, ParentClassTwo):
    ...

The ellipsis has the highest sorting level in csort, ensuring that such classes do not get reformatted.

Class docstrings
...............
Class docstrings are defined by the triple quote blocks immediately beneath the class definition.

Class docstrings have a fixed high order value to ensure that they are not reformatted.

.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     ...

Typed class attributes
.........................
Class attributes are data defined outside of a class method and are shared across all instances
of the class.

.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     name: str = "example"

In this example, the class attribute ``name`` is defined outside of any methods and is type annotated as a string.
Therefore, csort considers ``name`` to be a typed class attribute.

Typed class attributes have a higher sorting level than untyped class attributes.

Untyped class attributes
..................
.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     age = 50

In this example, the class attribute ``age`` is defined outside of any methods and is not type annotated.
Therefore, csort considers ``age`` to be an untyped class attribute.

If we have both typed and untyped class attributes then they will be re-ordered according to whether they are typed or
not and then alphabetically.

For example, this ``ExampleClass``:

.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     age = 50
     name: str = "Joe"
     pets: List[str] = ["dog", "cat"]
     last_name = "Bloggs"

would be converted to:
.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     pets: List[str] = ["dog", "cat"]
     name: str = "Joe"
     age = 50
     last_name = "Bloggs"


Methods
-------

Dunder methods
..............
Dunder methods, also known as magic methods or special methods, are a set of predefined methods in Python that
you can override to change the behavior of objects.

These methods allow objects to implement or emulate the behavior of built-in types and functions.

.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     def __init__(self, name: str) -> None
        self.name: str = name
        self.pets: List[str] = []

     def __len__(self) -> int:
        return len(self.pets)

In this example, two dunder methods are defined. By default, dunder methods are awarded the highest method sorting
level, ensuring that dunder methods always appear at the top of the class.

Classmethods
............
Class methods are methods that are bound to the class itself rather than to instances of the class.

They can be called on the class itself or on instances, and they have access to the class as their first argument,
which is conventionally named cls. This allows them to access and modify class state that applies across all instances
of the class.

Class methods are defined using the @classmethod decorator.

.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     name: str = "example"

     @classmethod
     def print_name(cls) -> None
        print(cls.name)

Staticmethods
.............
Static methods in Python are methods that belong to a class but do not access any instance or class-specific data.

They are defined using the @staticmethod decorator. Static methods are similar to regular functions but are included
in the class's namespace, making them accessible via the class name or instances of the class.

Static methods are often used for utility functions which are strongly tied to the overall class purpose.

.. code-block:: python

 class MathOperations:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

Properties
........
In Python, the @property decorator is used to define methods in a class that act like attributes.
These methods are typically used for managing the access to private attributes.

The @property decorator turns a method into a "getter" for a read-only attribute.

.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     def __init__(self, name: str) -> None
        self._name: str = name

     @property
     def name(self) -> str:
        return self._name

 example = ExampleClass(name="Steve")
 print(example.name)  # here _name is accessed using the name property

Getters
.......
The ``@property`` decorator is a pythonic way of creating a class property from scratch. The ``getter`` decorator
essentially does the same thing but using the ``<property>.getter`` syntax where ``<property>`` is the name of the
private attribute to access.

In general, the ``@property`` decorator is preferred when defining a property from scratch but the ``getter`` decorator
can be used when a subclass is modifying a property defined in a parent class.

.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     def __init__(self, name: str) -> None
        self._name: str = name

     @name.getter
     def name(self) -> str:
        return self._name

Setters
.......
Setters work in conjunction with ``@property`` and ``getter`` to support controlled access to private attributes.

The ``setter`` decorator allows controlled access whilst setting a new value.

.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     def __init__(self, name: str) -> None
        self._name: str = name

     @name.getter
     def name(self) -> str:
        return self._name

     @name.setter
     def name(self, new_name: str) -> None:
        self._name = name


Other decorated methods
.......................
Any decorated class method without any of the above mentioned decorators is considered by csort to be a
**decorated method**. This includes decorators such as ``abstractmethod``, ``functools.lru_cache``, ``singledispatch``.

Instance methods
................
Instance methods are method which have access to the ``self`` object of an instantiated class and can access and modify
instance attributes.

Instance methods are the standard python class method.

.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     def __init__(self, name: str) -> None
        self.name: str = name
        self.pets: List[str] = []

     def lower_name(self) -> str:
        return self.name.lower()

     def add_pet(self, new_pet: str) -> None:
        self.pets.append(new_pet)

``lower_name()`` and ``add_pet()`` are instance methods.

Private methods
...............
Private methods are often designated by starting with a single underscore ``_private_method()``.

Private methods are not supposed to be called outside of the class but are used by other methods of the class.

.. code-block:: python

 class ExampleClass:
     """
     This class is an example python class used in the csort documentation.
     """
     def __init__(self, first_name: str, last_name: str) -> None
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.pets: List[str] = []

     def full_name(self) -> str:
        return self._lower_first_name() + " " + self._lower_second_name()

     def _lower_first_name(self) -> str:
        return self.first_name.lower()

     def _lower_second_name(self) -> str:
        return self.second_name.lower()

In this example, ``_lower_first_name()`` and ``_lower_second_name()`` are private methods. By default, csort puts
private methods at the bottom of the class.
