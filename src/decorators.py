"""Functions for handling method decorators"""
import ast
from collections import defaultdict
from typing import Callable
from typing import Dict
from typing import Hashable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import libcst


class DecoratorDefaultDict(defaultdict):
    """
    Subclass of defaultdict to return length of this dictionary if provided key is missing

    Examples:
        d = DecoratorDefaultDict()
        d["key"] = "value"
        d["missing_key"]  # will return 1
    """

    def __init__(self) -> None:
        super().__init__(self.__class__)

    def __missing__(self, key: Hashable) -> int:
        return len(self)


# define here the ordering of decorated class functions
# any decorator not defined here will return the length of the dictionary
decorator_orders = DecoratorDefaultDict()
decorators = ["classmethod", "staticmethod", "property", "getter", "setter"]
for i, dec in enumerate(decorators):
    decorator_orders[dec] = i

# -------------------------------------------------------------------------
# AST functions
# -------------------------------------------------------------------------


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


def decorator_call_id(decorator: ast.Call) -> str:
    """
    Get the decorator type from an ast.Call decorator
    Args:
        decorator: input decorator

    Returns:
        attr attribute

    Raises:
        AttributeError: if decorator.func does not have id attribute
    """
    if hasattr(decorator.func, "id"):
        return decorator.func.id
    raise AttributeError("decorator of type ast.Call does not have func attribute with id attribute!")


# -------------------------------------------------------------------------
# CST functions
# -------------------------------------------------------------------------


def decorator_name_id_cst(decorator: libcst.Decorator) -> str:
    """
    Get the decorator type from an Name decorator
    Args:
        decorator: input decorator

    Returns:
        id attribute
    """
    if not hasattr(decorator.decorator, "value"):
        raise AttributeError("Could not find value attribute of decorator!")
    return decorator.decorator.value


def decorator_attribute_id_cst(decorator: libcst.Decorator) -> str:
    """
    Get the decorator type from an Attribute decorator
    Args:
        decorator: input decorator

    Returns:
        attr attribute
    """
    if not hasattr(decorator.decorator, "attr"):
        raise AttributeError("Could not find attr attribute of decorator!")
    return decorator.decorator.attr.value


def decorator_call_id_cst(decorator: libcst.Decorator) -> str:
    """
    Get the decorator type from an ast.Call decorator
    Args:
        decorator: input decorator

    Returns:
        attr attribute

    Raises:
        AttributeError: if decorator.func does not have id attribute
    """
    if isinstance(decorator.decorator, libcst.Call):
        if hasattr(decorator.decorator.func, "value"):
            return decorator.decorator.func.value
    raise AttributeError("libcst decorator of type libcst.Call does not have func attribute with value attribute!")


# factory to indicate what functions to call for describing different types of decorators
ast_decorator_description_factory: Dict[type, Callable] = {
    ast.Name: decorator_name_id,
    ast.Attribute: decorator_attribute_id,
    ast.Call: decorator_call_id,
}

cst_decorator_description_factory: Dict[type, Callable] = {
    libcst.Name: decorator_name_id_cst,
    libcst.Attribute: decorator_attribute_id_cst,
    libcst.Call: decorator_call_id_cst,
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
    func = ast_decorator_description_factory.get(type(decorator))
    if func is None:
        raise TypeError(f"Unexpected type {type(decorator)}!")
    return func(decorator)


def get_decorator_id_cst(decorator: libcst.Decorator) -> str:
    """
    Get the decorator type from a method decorator parsed by CST

    Args:
        decorator: input decorator expression

    Returns:
        type of decorator
    """
    func = cst_decorator_description_factory.get(type(decorator.decorator))
    if func is None:
        raise TypeError(f"Unexpected type {type(decorator)}!")
    return func(decorator)


def get_decorators(method: Union[ast.stmt, libcst.CSTNode], sort: bool = False) -> Optional[List[str]]:
    """
    Get decorators from an ast parsed function
    Args:
        method: the ast parsed method
        sort: if True, then decorators will be sorted according to decorator_orders

    Returns:
        list of ids from decorator list attribute
    """
    if isinstance(method, ast.stmt):
        return _get_decorators_ast(method, sort=sort)
    return _get_decorators_cst(method, sort=sort)


def _get_decorators_ast(method: ast.stmt, sort: bool = False) -> Optional[List[str]]:
    """
    Get decorators from an ast parsed function
    Args:
        method: the ast parsed method
        sort: if True, then decorators will be sorted according to decorator_orders

    Returns:
        list of ids from decorator list attribute
    """
    if not isinstance(method, ast.FunctionDef) or not hasattr(method, "decorator_list"):
        return None
    decorators = [get_decorator_id(decorator) for decorator in method.decorator_list]
    if sort:
        decorators = order_decorators(decorators)
    return decorators


def _get_decorators_cst(method: libcst.CSTNode, sort: bool = False) -> Optional[List[str]]:
    """
    Get decorators from an CST parsed function
    Args:
        method: the CST parsed method
        sort: if True, then decorators will be sorted according to decorator_orders

    Returns:
        list of ids from decorator list attribute
    """
    if not isinstance(method, libcst.FunctionDef) or not hasattr(method, "decorators"):
        return None
    decorators = [get_decorator_id_cst(decorator) for decorator in method.decorators]
    if sort:
        decorators = order_decorators(decorators)
    return decorators


def has_decorator(method: Union[ast.stmt, libcst.CSTNode], decorator: str) -> bool:
    """
    Determine if a parsed method has a specific decorator
    Args:
        method: the AST or CST parsed method node
        decorator: decorator to look for

    Returns:
        True if decorator in the decorators
    """
    decorators = _get_decorators_cst(method) if isinstance(method, libcst.CSTNode) else get_decorators(method)
    if decorators is None:
        return False
    return decorator in decorators


def _get_decorator_order(decorator: str) -> Tuple[int, str]:
    """
    Get the decorator order from decorator_orders

    A tuple if returned with the name to sort decorators alphabetically if the level is equal.
    Args:
        decorator: name of decorator

    Returns:
        (level of decorator, name of decorator)
    """
    return decorator_orders[decorator], decorator


def order_decorators(decorators: List[str]) -> List[str]:
    """
    Sort a list of decorators according to the pre-defined ordering in decorator_orders
    Args:
        decorators: list of decorators found for a method

    Returns:
        sorted decorators
    """
    return sorted(decorators, key=_get_decorator_order)
