"""Functions for handling CST parsed class components"""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import libcst

from .configs import DUNDER_PATTERN
from .configs import find_classes_response
from .configs import ordered_methods_type
from .decorators import get_decorators
from .edge_cases import handle_edge_cases
from .utilities import check_and_get_attribute
from .utilities import extract_text_from_file
from .utilities import is_class_docstring_cst
from .utilities import is_ellipsis_cst


def update_module(module: libcst.Module, classes: Dict[str, find_classes_response]) -> libcst.Module:
    """
    Update the libcst tree module with the formatted class nodes
    Args:
        module: libcst tree
        classes: mapping of class names to class nodes

    Returns:
        module: modified to include formatted classes
    """
    new_body = []
    for item in module.body:
        if isinstance(item, libcst.ClassDef):
            new_body.append(classes[item.name.value]["node"])
        else:
            new_body.append(item)
    module = module.with_changes(body=tuple(new_body))

    return module


def update_node(cls: find_classes_response, components: ordered_methods_type) -> find_classes_response:
    """
    Update CST class
    Args:
        cls: class definition to update
        components: sorted class components

    Returns:
        void

    Raises:
        TypeError: if classes contains nodes which are not class definitions
        AttributeError: if expected attributes of class definitions are not available
    """
    if not isinstance(cls["node"], (libcst.ClassDef, libcst.FunctionDef)):
        raise TypeError(f"Expected type libcst.ClassDef! Not {type(cls['node'])}")
    formatted_components = [
        update_node(find_classes_response(node=list(*m.items())[0], index=0), list(*m.items())[1])["node"]
        if isinstance(m, dict)
        else m
        for m in components
    ]
    cls["node"] = cls["node"].with_changes(body=cls["node"].body.with_changes(body=tuple(formatted_components)))
    return cls


def parse_code(code: Optional[str] = None, file_path: Optional[str] = None) -> libcst.Module:
    """
    Parse already loaded code with libcst module
    Args:
        code: input lines of code
        file_path: path to .py code

    Returns:
        parsed code as CST Module

    Raises:
        ValueError: if code and file_path are both None
    """
    if file_path is not None:
        code = extract_text_from_file(file_path)
    if code is not None:
        return libcst.parse_module(code)
    raise ValueError("Must provide code or file_path!")


def nodes_to_code(tree: libcst.Module, **kwargs: Any) -> str:  # pylint: disable=unused-argument
    """
    Unparse libcst tree to code string

    **kwargs provided for compatibility with ast_functions.nodes_to_code()

    Args:
        tree: libcst tree
        **kwargs: any other args

    Returns:
        source code string
    """
    code = tree.code_for_node(tree)
    code = handle_edge_cases(code, "cst")
    return code


def update_node_body(node: libcst.ClassDef, body: List[libcst.CSTNode]) -> libcst.ClassDef:
    """
    Update node with new body
    Args:
        node: libcst node to update
        body: the new body

    Returns:
        node: with updated body
    """
    node = node.with_changes(body=node.body.with_changes(body=tuple(body)))
    return node


def is_class(node: libcst.CSTNode) -> bool:
    """
    Determine if CST node is a class definition
    Args:
        node: input node

    Returns:
        True if node is a class definition
    """
    return isinstance(node, libcst.ClassDef)


def contains_class(node: libcst.FunctionDef) -> bool:
    """
    Determine if the body of a function definition contains an inner class
    Args:
        node: function definition node

    Returns:
        True if a class is defined in the function
    """
    if not hasattr(node, "body") or not hasattr(node.body, "body"):
        return False
    return any(is_class(child) for child in node.body.body)


def find_classes(module: libcst.Module) -> Dict[str, find_classes_response]:
    """
    Extract class definitions from libcst tree
    Args:
        module: libcst tree

    Returns:
        classes: a mapping of class names to class definition node and index in the tree body
    """
    classes = {
        node.name.value: find_classes_response(node=node, index=i)
        for i, node in enumerate(module.body)
        if is_class(node) and hasattr(node, "name")
    }
    return classes


def extract_class_components(class_node: Union[libcst.ClassDef, libcst.FunctionDef]) -> Sequence[libcst.CSTNode]:
    """
    Extract components of the class definition body
    Args:
        class_node: libcst class definition node

    Returns:
        tuple of class components e.g. function definitions, attributes, docstrings
    """
    if isinstance(class_node, libcst.FunctionDef):
        return class_node.body.body
    if not hasattr(class_node, "body"):
        return tuple()
    if not isinstance(class_node.body, libcst.IndentedBlock):
        raise TypeError("Expected class node body to be of type IndentedBlock!")
    components = [node for node in class_node.body.body if is_msortable(node)]
    return components


def is_dunder_method(method: libcst.CSTNode) -> bool:
    """
    Determine if the ast parsed method is a magic dunder method
    Args:
        method: the ast parsed method

    Returns:
        True if the method is dunder

    """
    name = check_and_get_attribute(method, "name")
    if name is None:
        return False
    return name.value.startswith(DUNDER_PATTERN) and name.value.endswith(DUNDER_PATTERN)


def is_annotated_class_attribute(expression: libcst.CSTNode) -> bool:
    """
    Determine if the CST parsed expression is a type annotated class attribute

    e.g.
    class MyClass:
        name: str = "myclass"
        id = 1

    name would return True as it is typed as a string.
    id would return False as it is untyped

    Args:
        expression: the cst parsed expression

    Returns:
        True if the expression is a type annotated attribute

    """
    if not isinstance(expression, libcst.SimpleStatementLine):
        return False
    return isinstance(expression.body[0], libcst.AnnAssign)


def is_class_attribute(expression: libcst.CSTNode) -> bool:
    """
    Determine if the cst parsed expression is a untyped class attribute

    e.g.
    class MyClass:
        name: str = "myclass"
        id = 1

    name would return False as it is typed as a string.
    id would return True as it is untyped

    Args:
        expression: the cst parsed expression

    Returns:
        True if the expression is a untyped attribute

    """
    if not isinstance(expression, libcst.SimpleStatementLine):
        return False
    return isinstance(expression.body[0], libcst.Assign)


def is_private_method(method: libcst.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a private method - i.e. starts with "_"
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a private method
    """
    return method.name.value.startswith("_") and not is_dunder_method(method)


def is_function(expression: libcst.CSTNode) -> bool:
    """
    Determine if the ast parsed expression is a function definition

    Args:
        expression: the ast parsed expression

    Returns:
        True if the expression is a function definition

    """
    return isinstance(expression, libcst.FunctionDef)


def is_decorated(expression: libcst.CSTNode) -> bool:
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


def is_msortable(expression: libcst.CSTNode) -> bool:
    """
    Determine if the ast parsed expression is sortable by msort

    Defines a list of checks and if any of the checks evaluate as True, then the expression can be sorted.

    Args:
        expression: the ast parsed expression

    Returns:
        True if the expression is sortable

    """
    checks = [
        is_class,
        is_function,
        is_ellipsis_cst,
        is_annotated_class_attribute,
        is_class_attribute,
        is_class_docstring_cst,
    ]
    return any(func(expression) for func in checks)
