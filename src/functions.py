"""Functions for handling ast parsed class methods"""
import ast
from collections import OrderedDict
from typing import Callable
from typing import Dict

from src.configs import DUNDER_PATTERN
from src.configs import INSTANCE_METHOD_LEVEL
from src.decorators import get_decorators


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
        return constant_value.__str__() == "Ellipsis"
    return False


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


method_checking_map: Dict[Callable, int] = OrderedDict(
    [
        (is_ellipsis, 0),
        (is_dunder_method, 0),
        (is_class_method, 1),
        (is_static_method, 2),
        (is_property, 3),
        (is_getter, 4),
        (is_setter, 5),
        (is_private_method, 7),
    ]
)


def get_method_type(method: ast.stmt) -> int:
    """
    Get the ordering level of the method
    Args:
        method: input ast parsed method

    Returns:
        level: integer used to order the methods
    """
    for func, level in method_checking_map.items():
        if func(method):
            return level
    return INSTANCE_METHOD_LEVEL
