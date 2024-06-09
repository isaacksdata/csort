"""Functions for handling AST parsed class components"""
import ast
from collections import OrderedDict
from copy import deepcopy
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

import ast_comments
import astor

from .configs import DUNDER_PATTERN
from .configs import find_classes_response
from .decorators import get_decorators
from .edge_cases import handle_edge_cases
from .generic_functions import is_class_method
from .generic_functions import is_csort_group
from .generic_functions import is_getter
from .generic_functions import is_property
from .generic_functions import is_setter
from .generic_functions import is_static_method
from .imports import handle_import_formatting
from .utilities import is_class_docstring
from .utilities import is_ellipsis
from .utilities import merge_code_strings
from .utilities import remove_comment_nodes


def update_module(module: ast.Module, classes: Dict[str, find_classes_response]) -> ast.Module:
    """
    Update the ast tree module with the formatted class nodes
    Args:
        module: ast tree
        classes: mapping of class names to class nodes

    Returns:
        module: modified to include formatted classes

    Raises:
        TypeError: if class node is not of tye ast.stmt
    """
    for _, cls in classes.items():
        if not isinstance(cls["node"], ast.stmt):
            raise TypeError("Trying to assign incompatible node to ast module!")
        module.body[cls["index"]] = cls["node"]
    return module


def update_node(cls: find_classes_response, components: List[ast.stmt]) -> find_classes_response:
    """
    Update AST class
    Args:
        cls: class definition to update
        components: sorted class components

    Returns:
        cls: class node updated with sorted components

    Raises:
        AttributeError: if class node does not have body attribute
    """
    if not hasattr(cls["node"], "body"):
        raise AttributeError("Class definition does not have body attribute!")
    components = [
        update_node(find_classes_response(node=list(*m.items())[0], index=0), list(*m.items())[1])["node"]
        if isinstance(m, dict)
        else m
        for m in components
    ]
    cls["node"].body = components
    return cls


def parse_code(code: Optional[str] = None, file_path: Optional[str] = None) -> ast.Module:
    """
    Parse already loaded code with ast module
    Args:
        code: input lines of code
        file_path: path to .py code

    Returns:
        parsed code as ast Module

    Raises:
        ValueError: if code and file_path are both None
    """
    if code is not None:
        return ast_comments.parse(code)
    if file_path is not None:
        return astor.parse_file(file_path)
    raise ValueError("Must provide code or file_path!")


def nodes_to_code(tree: ast.Module, source_code: str) -> str:
    """
    Unparse AST tree to source code.

    Handle edge cases to ensure full reproducibility of source code:
    1) merges back comments lost during AST parsing
    2) handles line spacing
    3) handles import spacing

    Args:
        tree: AST tree
        source_code: original python code string

    Returns:
        new_code: source code strings after formatting
    """
    new_code = preserve_comments(tree)
    new_code = handle_edge_cases(new_code, "ast")
    new_code = handle_import_formatting(source_code=source_code, ast_code=new_code)
    return new_code


def find_classes(code: ast.Module) -> Dict[str, find_classes_response]:
    """
    Find all class definitions within parsed code
    Args:
        code: parsed code module

    Returns:
        classes: list of class definitions
    """
    classes = {}

    # Find all function definitions
    for i, node in enumerate(code.body):
        if is_class(node) and hasattr(node, "name"):
            classes[node.name] = find_classes_response(node=node, index=i)
    return classes


def extract_class_components(code: ast.ClassDef) -> List[ast.stmt]:
    """
    Find all method definitions within a class definition
    Args:
        code: parsed class definition

    Returns:
        functions: list of function definitions
    """
    functions: List[ast.stmt] = []

    # Find all function definitions
    for node in code.body:
        if is_csortable(node):
            functions.append(node)
    return functions


def is_class(expression: ast.AST) -> bool:
    """
    Determine if AST parsed expression is a class definition
    Args:
        expression: AST expression

    Returns:
        True if represents a class definition
    """
    return isinstance(expression, ast.ClassDef)


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


def is_private_method(method: ast.FunctionDef) -> bool:
    """
    Determine if the ast parsed method is a private method - i.e. starts with "_"
    Args:
        method: the ast parsed method

    Returns:
        True if the method is a private method
    """
    return method.name.startswith("_") and not is_dunder_method(method)


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
        is_class,
        is_function,
        is_ellipsis,
        is_annotated_class_attribute,
        is_class_attribute,
        is_class_docstring,
    ]
    return any(func(expression) for func in checks)


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


def preserve_comments(parsed_code: ast.Module) -> str:
    """
    Preserve comments by merging the code derived from astor and ast_comments libraries.

    Astor is better at preserving indentations and line breaks.
    Ast_comments captures comments but the comments cannot be unparsed with astor.
    Args:
        parsed_code: ast tree

    Returns:
        new_code: merged code from astor and ast_comments parsers
    """
    uncommented_code = deepcopy(parsed_code)
    uncommented_code = remove_comment_nodes(uncommented_code)
    astor_code = astor.to_source(uncommented_code)
    new_code = ast_comments.unparse(parsed_code)
    new_code = merge_code_strings(astor_code, new_code)
    return new_code
