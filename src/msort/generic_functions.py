import ast
from typing import Union

import libcst

from .decorators import has_decorator


def is_msort_group(method: Union[ast.FunctionDef, libcst.CSTNode]) -> bool:
    """
    Determine if the ast parsed method is a msort_group method - i.e. used the @msort_group() decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method has been assigned a msort group
    """
    return has_decorator(method, "msort_group")


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


def is_deleter(method: Union[ast.FunctionDef, libcst.CSTNode]) -> bool:
    """
    Determine if the ast parsed method is a deleter - i.e. used the @deleter decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a deleter
    """
    return has_decorator(method, "deleter")
