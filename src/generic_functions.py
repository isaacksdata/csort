import ast
from typing import Union

import libcst

from src.decorators import has_decorator


def is_csort_group(method: Union[ast.FunctionDef, libcst.CSTNode]) -> bool:
    """
    Determine if the ast parsed method is a csort_group method - i.e. used the @csort_group() decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method has been assigned a csort group
    """
    return has_decorator(method, "csort_group")


def is_class_method(method: Union[ast.FunctionDef, libcst.CSTNode]) -> bool:
    """
    Determine if the parsed method is a class method - i.e. used the @classmethod decorator
    Args:
        method: the parsed method

    Returns:
        True if the method is a class method
    """
    return has_decorator(method, "classmethod")


def is_static_method(method: Union[ast.FunctionDef, libcst.CSTNode]) -> bool:
    """
    Determine if the ast parsed method is a static method - i.e. used the @staticmethod decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a static method
    """
    return has_decorator(method, "staticmethod")


def is_property(method: Union[ast.FunctionDef, libcst.CSTNode]) -> bool:
    """
    Determine if the ast parsed method is a property - i.e. used the @property decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a property
    """
    return has_decorator(method, "property")


def is_setter(method: Union[ast.FunctionDef, libcst.CSTNode]) -> bool:
    """
    Determine if the ast parsed method is a setter - i.e. used the @setter decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a setter
    """
    return has_decorator(method, "setter")


def is_getter(method: Union[ast.FunctionDef, libcst.CSTNode]) -> bool:
    """
    Determine if the ast parsed method is a getter - i.e. used the @getter decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a getter
    """
    return has_decorator(method, "getter")
