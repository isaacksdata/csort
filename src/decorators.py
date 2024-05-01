"""Functions for handling method decorators"""
import ast
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional


def decorator_name_id(decorator: ast.Name) -> str:
    """
    Get the decorator type from an ast.Name decorator
    Args:
        decorator: input decorator

    Returns:
        id attribute
    """
    return decorator.id


def decorator_attribute_id(decorator: ast.Attribute) -> str:
    """
    Get the decorator type from an ast.Attribute decorator
    Args:
        decorator: input decorator

    Returns:
        attr attribute
    """
    return decorator.attr


decorator_description_factory: Dict[type, Callable] = {
    ast.Name: decorator_name_id,
    ast.Attribute: decorator_attribute_id,
}


def get_decorator_id(decorator: ast.expr) -> str:
    """
    Get the decorator type from a method decorator parsed by ast

    This function uses decorator_description_factory to find the correct attribute given the type of ast expression.
    Args:
        decorator: input decorator expression

    Returns:
        type of decorator
    """
    func = decorator_description_factory.get(type(decorator))
    if func is None:
        raise TypeError(f"Unexpected type {type(decorator)}!")
    return func(decorator)


def get_decorators(method: ast.stmt) -> Optional[List[str]]:
    """
    Get decorators from an ast parsed function
    Args:
        method: the ast parsed method

    Returns:
        list of ids from decorator list attribute
    """
    if not isinstance(method, ast.FunctionDef) or not hasattr(method, "decorator_list"):
        return None
    return [get_decorator_id(decorator) for decorator in method.decorator_list]


def has_decorator(method: ast.stmt, decorator: str) -> bool:
    decorators = get_decorators(method)
    if decorators is None:
        return False
    return decorator in decorators
