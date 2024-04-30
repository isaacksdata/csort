"""Functions for handling ast parsed class methods"""
import ast
from collections import OrderedDict
from typing import Callable
from typing import Dict
from typing import Tuple

from src.configs import DUNDER_PATTERN
from src.configs import INSTANCE_METHOD_LEVEL
from src.decorators import get_decorators
from src.utilities import get_expression_name


def is_ellipsis(expression: ast.AST) -> bool:
    """
    Determine if a class has an empty body - use of ...

    e.g.

    class MyClass(MyMixin, MyBaseClass):
        ...

    Args:
        expression: ast parsed expression

    Returns:
        True if the expression is an Ellipsis
    """
    if not hasattr(expression, "value"):
        return False
    expression_value = expression.value
    if isinstance(expression_value, ast.Constant):
        constant_value = expression_value.value
        return str(constant_value) == "Ellipsis"
    return False


def is_annotated_class_attribute(expression: ast.AST) -> bool:
    """
    Determine if the ast parsed expression is a type annotated class attribute

    e.g.
    class MyClass:
        name: str = "myclass"
        id = 1

    name would return True as it is typed as a string.
    id would return False as it is untyped

    Args:
        expression: the ast parsed expression

    Returns:
        True if the expression is a type annotated attribute

    """
    return isinstance(expression, ast.AnnAssign)


def is_class_attribute(expression: ast.AST) -> bool:
    """
    Determine if the ast parsed expression is a untyped class attribute

    e.g.
    class MyClass:
        name: str = "myclass"
        id = 1

    name would return False as it is typed as a string.
    id would return True as it is untyped

    Args:
        expression: the ast parsed expression

    Returns:
        True if the expression is a untyped attribute

    """
    return isinstance(expression, ast.Assign)


def is_dunder_method(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a magic dunder method
    Args:
        method: the ast parsed method

    Returns:
        True if the method is dunder

    """
    return method.name.startswith(DUNDER_PATTERN) and method.name.endswith(DUNDER_PATTERN)


def is_class_method(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a class method - i.e. used the @classmethod decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a class method
    """
    return "classmethod" in get_decorators(method)


def is_static_method(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a static method - i.e. used the @staticmethod decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a static method
    """
    return "staticmethod" in get_decorators(method)


def is_property(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a property - i.e. used the @property decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a property
    """
    return "property" in get_decorators(method)


def is_setter(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a setter - i.e. used the @setter decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a setter
    """
    return "setter" in get_decorators(method)


def is_getter(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a getter - i.e. used the @getter decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a getter
    """
    return "getter" in get_decorators(method)


def is_private_method(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a private method - i.e. starts with "_"
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a private method
    """
    return method.name.startswith("_")


def is_function(expression: ast.AST) -> bool:
    """
    Determine if the ast parsed expression is a function definition

    Args:
        expression: the ast parsed expression

    Returns:
        True if the expression is a function definition

    """
    return isinstance(expression, ast.FunctionDef)


def is_csortable(expression: ast.AST) -> bool:
    """
    Determine if the ast parsed expression is sortable by Csort

    Defines a list of checks and if any of the checks evaluate as True, then the expression can be sorted.

    Args:
        expression: the ast parsed expression

    Returns:
        True if the expression is sortable

    """
    checks = [is_function, is_ellipsis, is_annotated_class_attribute, is_class_attribute]
    return any(func(expression) for func in checks)


method_checking_map: Dict[Callable, int] = OrderedDict(
    [
        (is_ellipsis, 0),
        (is_annotated_class_attribute, 0),
        (is_class_attribute, 1),
        (is_dunder_method, 2),
        (is_class_method, 3),
        (is_static_method, 4),
        (is_property, 5),
        (is_getter, 6),
        (is_setter, 7),
        (is_private_method, 9),
    ]
)


def get_method_type(method: ast.stmt) -> int:
    """
    Get the ordering level of the method type
    Args:
        method: the method to get the ordering level of

    Returns:
        level: sorting level of the method
    """
    for func, level in method_checking_map.items():
        if func(method):
            return level
    return INSTANCE_METHOD_LEVEL


def get_method_type_and_name(method: ast.stmt) -> Tuple[int, str]:
    """
    Get the ordering level of the method and the method name
    Args:
        method: input ast parsed method

    Returns:
        level: integer used to order the methods
        name: assigned name of the expression
    """
    name = get_expression_name(method)
    level = get_method_type(method)
    return level, name
