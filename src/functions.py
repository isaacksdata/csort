"""Functions for handling ast parsed class methods"""
import ast
import configparser
import logging
from abc import ABC
from abc import abstractmethod
from collections import OrderedDict
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from src.configs import DEFAULT_CSORT_ORDER_PARAMS
from src.configs import DUNDER_PATTERN
from src.configs import INSTANCE_METHOD_LEVEL
from src.decorators import get_decorators
from src.decorators import has_decorator
from src.utilities import get_expression_name
from src.utilities import is_class_docstring
from src.utilities import is_ellipsis


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


def is_csort_group(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a csort_group method - i.e. used the @csort_group() decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method has been assigned a csort group
    """
    return has_decorator(method, "csort_group")


def is_class_method(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a class method - i.e. used the @classmethod decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a class method
    """
    return has_decorator(method, "classmethod")


def is_static_method(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a static method - i.e. used the @staticmethod decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a static method
    """
    return has_decorator(method, "staticmethod")


def is_property(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a property - i.e. used the @property decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a property
    """
    return has_decorator(method, "property")


def is_setter(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a setter - i.e. used the @setter decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a setter
    """
    return has_decorator(method, "setter")


def is_getter(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a getter - i.e. used the @getter decorator
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a getter
    """
    return has_decorator(method, "getter")


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


def is_decorated(expression: ast.stmt) -> bool:
    """
    Determine if the ast parsed expression is decorated.

    Args:
        expression: the ast parsed expression

    Returns:
        True if the expression has a decorator

    """
    decorators = get_decorators(expression)
    if decorators is None or len(decorators) == 0:
        return False
    return True


def is_csortable(expression: ast.AST) -> bool:
    """
    Determine if the ast parsed expression is sortable by Csort

    Defines a list of checks and if any of the checks evaluate as True, then the expression can be sorted.

    Args:
        expression: the ast parsed expression

    Returns:
        True if the expression is sortable

    """
    checks = [
        is_function,
        is_ellipsis,
        is_annotated_class_attribute,
        is_class_attribute,
        is_class_docstring,
    ]
    return any(func(expression) for func in checks)


# todo this needs to be mapped from the config file
method_checking_map: Dict[Callable, int] = OrderedDict(
    [
        (is_ellipsis, 0),
        (is_class_docstring, 0),
        (is_annotated_class_attribute, 1),
        (is_class_attribute, 2),
        (is_dunder_method, 3),
        (is_csort_group, 4),
        (is_class_method, 5),
        (is_static_method, 6),
        (is_property, 7),
        (is_getter, 8),
        (is_setter, 9),
        (is_decorated, 10),
        (is_private_method, 12),
    ]
)


class MethodDescriber(ABC):
    """
    Abstract class for describing a method of a class

    Attributes:
        _config: contains configurations from config file
        _config_to_func_map: a mapping from config keys to the appropriate function
        _method_checking_map: a mapping of a function to an ordering level
    """

    def __init__(self, config: configparser.ConfigParser) -> None:
        self._config = config
        self._config_to_func_map: Dict[str, Callable] = self._setup_config_to_func_map()
        self._method_checking_map: Dict[Callable, int] = self._setup_func_to_level_map()
        self._instance_method_default: int = INSTANCE_METHOD_LEVEL

    @abstractmethod
    def _setup_func_to_level_map(self) -> Dict[Callable, int]:
        pass

    @abstractmethod
    def _validate_node(self, node: Any) -> bool:
        """
        Validate that a representation of some code can be used with this instance of MethodDescriber
        Args:
            node: the code representation

        Returns:
            True if the code is compatible
        """
        pass

    @abstractmethod
    def _setup_config_to_func_map(self) -> Dict[str, Callable]:
        pass

    def get_method_type(self, method: Any, use_csort_group: bool = True) -> int:
        """
        Get the ordering level of the method type
        Args:
            method: the method to get the ordering level of
            use_csort_group: If True, then will check for csort_group

        Returns:
            level: sorting level of the method

        Raises:
            TypeError: if incompatible code representation used
        """
        if not self._validate_node(method):
            raise TypeError(f"Node of type {type(method)} cannot be used!")
        for func, level in self._method_checking_map.items():
            if func.__name__ == "is_csort_group" and not use_csort_group:
                continue
            if func(method):
                return level
        return self._instance_method_default


class ASTMethodDescriber(MethodDescriber):
    """
    Concrete class for describing methods of classes where the methods have been parsed using AST tree.
    """

    def _validate_node(self, node: Any) -> bool:
        """
        Validate that the node is instance of ast.AST
        Args:
            node: AST node for some source code

        Returns:
            True if the node is of type ast.AST
        """
        return isinstance(node, ast.AST)

    def _setup_config_to_func_map(self) -> Dict[str, Callable]:
        """
        Setting up the mapping from csort config to AST function classifying functions
        Returns:
            The mapping of config variables to a Callable function
        """
        return {
            "dunder_method": is_dunder_method,
            "csort_group": is_csort_group,
            "class_method": is_class_method,
            "static_method": is_static_method,
            "property": is_property,
            "getter": is_getter,
            "setter": is_setter,
            "decorated_method": is_decorated,
            "private_method": is_private_method,
        }

    @staticmethod
    def _non_method_defaults() -> List[Tuple[Callable, int]]:
        """
        Set up fixed mapping from AST functions to ordering level.

        The ordering level does not change for these node types.
        Returns:
            Mapping from fixed node types to order level
        """
        return [
            (is_ellipsis, 0),
            (is_class_docstring, 0),
            (is_annotated_class_attribute, 1),
            (is_class_attribute, 2),
        ]

    def _setup_func_to_level_map(self) -> Dict[Callable, int]:
        """
        Set up a full mapping from AST function classifying function to ordering level.

        1) Fixed defaults are added
        2) User defined ordering levels from the config file are added
        3) Any node types missing from the config are added using default values
        4) Sort the mapping according to ordering level and put into OrderedDict
        Returns:
            func_to_value_map: OrderedDict with node classifying functions as keys and ordering levels as values
        """
        configs = self._config["csort.order"]
        if "instance_method" in configs:
            self._instance_method_default = int(configs.pop("instance_method"))

        mapping: List[Tuple[Callable, int]] = []

        mapping.extend(self._non_method_defaults())
        mapping.extend([(self._config_to_func_map[method], int(value)) for method, value in configs.items()])

        # check if need to add any defaults
        for method_type, value in DEFAULT_CSORT_ORDER_PARAMS.items():
            if method_type == "instance_method":
                continue
            if self._config_to_func_map[method_type] not in map(lambda t: t[0], mapping):
                logging.info("Using default level %s for %s", value, method_type)
                mapping.append((self._config_to_func_map[method_type], value))
        mapping = sorted(mapping, key=lambda t: t[1])
        func_to_value_map: Dict[Callable, int] = OrderedDict(mapping)

        return func_to_value_map


def describe_method(
    method: ast.stmt, method_describer: MethodDescriber
) -> Tuple[Tuple[int, int], Optional[List[str]], str]:
    """
    Get the ordering level of the method and the method name
    Args:
        method: input ast parsed method
        method_describer: instance of a MethodDescriber subclass which can map methods of classes to an order level

    Returns:
        level: integer used to order the methods
        name: assigned name of the expression
    """
    name = get_expression_name(method)
    level = method_describer.get_method_type(method, use_csort_group=True)
    decorators = get_decorators(method, sort=True)
    if decorators is not None and "csort_group" in decorators:
        second_level = method_describer.get_method_type(method, use_csort_group=False)
        decorators.remove("csort_group")
    else:
        second_level = level
    return (level, second_level), decorators, name
