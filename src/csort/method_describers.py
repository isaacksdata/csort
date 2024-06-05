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
from typing import Union

import libcst

from . import ast_functions as AST
from . import cst_functions as CST
from . import generic_functions as GEN
from .configs import DEFAULT_CSORT_ORDER_PARAMS
from .configs import DEFAULT_CSORT_PARAMS_SECTION
from .configs import INSTANCE_METHOD_LEVEL
from .decorators import get_decorators
from .utilities import get_expression_name
from .utilities import is_class_docstring
from .utilities import is_class_docstring_cst
from .utilities import is_ellipsis
from .utilities import is_ellipsis_cst


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

    @staticmethod
    @abstractmethod
    def _non_method_defaults() -> List[Tuple[Callable, int]]:
        """
        Set up fixed mapping from AST functions to ordering level.

        The ordering level does not change for these node types.
        Returns:
            Mapping from fixed node types to order level
        """
        pass

    @property
    def use_csort_group(self) -> bool:
        """
        Property method to access the use_csort_group param of the csort config
        Returns:
            True if Csort should consider the csort_group decorator
        """
        param = self._config[DEFAULT_CSORT_PARAMS_SECTION]["use_csort_group"]
        return ast.literal_eval(param) if isinstance(param, str) else param

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

    @abstractmethod
    def _setup_config_to_func_map(self) -> Dict[str, Callable]:
        pass

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
            "dunder_method": AST.is_dunder_method,
            "csort_group": GEN.is_csort_group,
            "class_method": GEN.is_class_method,
            "static_method": GEN.is_static_method,
            "property": GEN.is_property,
            "getter": GEN.is_getter,
            "setter": GEN.is_setter,
            "decorated_method": AST.is_decorated,
            "private_method": AST.is_private_method,
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
            (AST.is_annotated_class_attribute, 1),
            (AST.is_class_attribute, 2),
        ]


class CSTMethodDescriber(MethodDescriber):
    """
    Concrete class for describing methods of classes where the methods have been parsed using CST tree.
    """

    def _validate_node(self, node: Any) -> bool:
        """
        Validate that the node is instance of libcst.CSTNode
        Args:
            node: CST node for some source code

        Returns:
            True if the node is of type libcst.CSTNode
        """
        return isinstance(node, libcst.CSTNode)

    def _setup_config_to_func_map(self) -> Dict[str, Callable]:
        """
        Setting up the mapping from csort config to AST function classifying functions
        Returns:
            The mapping of config variables to a Callable function
        """
        return {
            "dunder_method": CST.is_dunder_method,
            "csort_group": GEN.is_csort_group,
            "class_method": GEN.is_class_method,
            "static_method": GEN.is_static_method,
            "property": GEN.is_property,
            "getter": GEN.is_getter,
            "setter": GEN.is_setter,
            "decorated_method": CST.is_decorated,
            "private_method": CST.is_private_method,
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
            (is_ellipsis_cst, 0),
            (is_class_docstring_cst, 0),
            (CST.is_annotated_class_attribute, 1),
            (CST.is_class_attribute, 2),
        ]


method_describers: Dict[str, Callable] = {"ast": ASTMethodDescriber, "cst": CSTMethodDescriber}


def get_method_describer(parser_type: str, **kwargs: Any) -> MethodDescriber:
    if parser_type not in method_describers:
        raise KeyError(f"Unknown type of method describer requested : {parser_type}")
    return method_describers[parser_type](**kwargs)


def describe_method(
    method: Union[ast.stmt, libcst.CSTNode], method_describer: MethodDescriber
) -> Tuple[Tuple[int, int], Optional[List[str]], str]:
    """
    Get the ordering level of the method and the method name
    Args:
        method: input AST or CST parsed method
        method_describer: instance of a MethodDescriber subclass which can map methods of classes to an order level

    Returns:
        level: integer used to order the methods
        name: assigned name of the expression
    """
    name = get_expression_name(method)
    level = method_describer.get_method_type(method, use_csort_group=method_describer.use_csort_group)
    decorators = get_decorators(method, sort=True)
    if decorators is not None and "csort_group" in decorators and method_describer.use_csort_group:
        second_level = method_describer.get_method_type(method, use_csort_group=False)
        decorators.remove("csort_group")
    else:
        second_level = level
    return (level, second_level), decorators, name
