import ast
import logging
import os
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import TypeVar
from typing import Union

import ast_comments
import astor
import libcst

from .configs import DOCSTRING_NAME


T = TypeVar("T")


def check_and_get_attribute(obj: T, attribute: str, raise_exception: bool = False) -> Any:
    output = hasattr(obj, attribute)
    if not output and raise_exception:
        raise AttributeError(f"Object of type {type(obj)} does not have the attribute {attribute}!")
    return getattr(obj, attribute, None)


def extract_text_from_file(file_path: str) -> str:
    """
    Load text from a file
    Args:
        file_path: path to file

    Returns:
        python_code: code from the file
    """
    with open(file_path, "r", encoding="utf-8") as f:
        python_code = f.read()
        return python_code


def get_function_name(method: Union[ast.FunctionDef, libcst.FunctionDef]) -> str:
    """
    Wrapper function for extracting a function name from AST or CST parsed code
    Args:
        method: node to get function name from

    Returns:
        function name
    """
    if isinstance(method, ast.FunctionDef):
        return get_function_name_ast(method)
    return get_expression_name_cst(method)


def get_function_name_ast(method: ast.FunctionDef) -> str:
    """
    Extract name from ast parsed function

    Examples:
        def func(self):
            ...

        get_function_name returns 'func'

    Args:
        method: ast parsed function

    Returns:
        name of the function
    """
    return method.name


def get_function_name_cst(method: libcst.FunctionDef) -> str:
    """
    Extract name from CST parsed function

    Examples:
        def func(self):
            ...

        get_function_name returns 'func'

    Args:
        method: CST parsed function

    Returns:
        name of the function
    """
    return method.name.value


def get_annotated_attribute_name(attribute: ast.AnnAssign) -> str:
    """
    Extract name from ast parsed annotated attribute

    Examples:
        class MyClass:
            name: str = "myclass"

        get_annotated_attribute_name returns 'name'

    Args:
        attribute: ast parsed attribute

    Returns:
        name of the attribute

    Raises:
        AttributeError: if the target does not have id attribute
    """
    return check_and_get_attribute(attribute.target, "id", raise_exception=True)


def get_annotated_attribute_name_cst(attribute: libcst.AnnAssign) -> str:
    """
    Extract name from ast parsed annotated attribute

    Examples:
        class MyClass:
            name: str = "myclass"

        get_annotated_attribute_name returns 'name'

    Args:
        attribute: ast parsed attribute

    Returns:
        name of the attribute

    Raises:
        TypeError: if attribute is not annotated attribute type
        AttributeError: if the target does not have id attribute
    """
    if not isinstance(attribute, libcst.SimpleStatementLine) or not isinstance(attribute.body[0], libcst.AnnAssign):
        raise TypeError("Attribute is not annotated attribute!")
    return check_and_get_attribute(attribute.body[0].target, "value", raise_exception=True)


def get_attribute_name(attribute: ast.Assign) -> str:
    """
    Extract name from ast parsed unannotated attribute

    Examples:
        class MyClass:
            name = "myclass"

        get_attribute_name returns 'name'

    Args:
        attribute: ast parsed attribute

    Returns:
        name of the attribute

    Raises:
        ValueError: if the targets attribute is empty
        AttributeError: if the target does not have id attribute
    """
    if len(attribute.targets) == 0:
        raise ValueError("No targets found for the attribute")
    return check_and_get_attribute(attribute.targets[0], "id", raise_exception=True)


def get_attribute_name_cst(attribute: libcst.Assign) -> str:
    """
    Extract name from ast parsed attribute

    Examples:
        class MyClass:
            name = "myclass"

        get_attribute_name returns 'name'

    Args:
        attribute: ast parsed attribute

    Returns:
        name of the attribute

    Raises:
        TypeError: if attribute is not of type libcst.Assign
        AttributeError: if the target does not have id attribute
    """
    if not isinstance(attribute, libcst.SimpleStatementLine) or not isinstance(attribute.body[0], libcst.Assign):
        raise TypeError("Attribute is not attribute!")
    target = check_and_get_attribute(attribute.body[0].targets[0], "target", raise_exception=True)
    return target.value


def get_ellipsis_name(expression: Union[ast.Expr, libcst.CSTNode]) -> str:
    """
    Extract name from an Ellipsis node
    Args:
        expression: ellipsis expression

    Returns:
        name
    """
    if isinstance(expression, libcst.CSTNode):
        return "ellipsis"
    return str(check_and_get_attribute(expression.value, "value", raise_exception=True))


names_factory: Dict[type, Callable] = {
    ast.FunctionDef: get_function_name_ast,
    ast.AnnAssign: get_annotated_attribute_name,
    ast.Assign: get_attribute_name,
    ast.ClassDef: get_function_name_ast,
}


cst_names_factory: Dict[type, Callable] = {
    libcst.FunctionDef: get_function_name_cst,
    libcst.AnnAssign: get_annotated_attribute_name_cst,
    libcst.Assign: get_attribute_name_cst,
    libcst.ClassDef: get_function_name_cst,
}


def get_expression_name(expression: Union[ast.stmt, libcst.CSTNode]) -> str:
    """
    Extract name from ast parsed expression

    Args:
        expression: ast parsed expression

    Returns:
        name of the expression
    """
    if isinstance(expression, ast.stmt):
        return get_expression_name_ast(expression)
    return get_expression_name_cst(expression)


def get_expression_name_ast(expression: ast.stmt) -> str:
    """
    Extract name from ast parsed expression

    Args:
        expression: ast parsed expression

    Returns:
        name of the expression
    """
    if is_ellipsis(expression) and isinstance(expression, ast.Expr):
        return get_ellipsis_name(expression)
    if is_class_docstring(expression) and isinstance(expression, ast.Expr):
        return DOCSTRING_NAME
    return names_factory[type(expression)](expression)


def get_expression_name_cst(expression: libcst.CSTNode) -> str:
    """
    Extract name from ast parsed expression

    Args:
        expression: ast parsed expression

    Returns:
        name of the expression
    """
    if is_ellipsis_cst(expression) and isinstance(expression, libcst.SimpleStatementLine):
        return get_ellipsis_name(expression)
    if is_class_docstring_cst(expression) and isinstance(expression, libcst.SimpleStatementLine):
        return DOCSTRING_NAME

    expr_type: type
    if isinstance(expression, libcst.SimpleStatementLine):
        expr_type = type(expression.body[0])
    else:
        expr_type = type(expression)
    return cst_names_factory[expr_type](expression)


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
    expression_value = check_and_get_attribute(expression, "value")
    if expression_value is None:
        return False
    if isinstance(expression_value, ast.Constant):
        constant_value = expression_value.value
        return str(constant_value) == "Ellipsis"
    return False


def is_ellipsis_cst(expression: libcst.CSTNode) -> bool:
    """
    Determine if a class has an empty body - use of ...

    e.g.

    class MyClass(MyMixin, MyBaseClass):
        ...

    Args:
        expression: CST parsed expression

    Returns:
        True if the expression is an Ellipsis
    """
    if not isinstance(expression, libcst.SimpleStatementLine):
        return False
    if not isinstance(expression.body[0], libcst.Expr):
        return False
    return isinstance(expression.body[0].value, libcst.Ellipsis)


def is_class_docstring(expression: ast.AST) -> bool:
    """
    Determine if an expression is a class docstring

    A class docstring is defined by triple double or single quotes.

    Args:
        expression: ast parsed expression

    Returns:
        True if the expression is a docstring

    Raises:
        AttributeError: if astor.to_source fails and its not due to the node representing a Comment

    """
    try:
        s: str = astor.to_source(expression)
    except AttributeError as e:
        if str(e) == "No defined handler for node of type Comment":
            logging.debug("Comments are not supported by astor")
            return False
        raise
    return (s.startswith('"""') and s.endswith('"""\n')) or (s.startswith("'''") and s.endswith("'''\n"))


def is_class_docstring_cst(expression: libcst.CSTNode) -> bool:
    """
    Determine if an expression is a class docstring

    A class docstring is defined by triple double or single quotes.

    Args:
        expression: CST parsed expression

    Returns:
        True if the expression is a docstring

    """
    if not isinstance(expression, libcst.SimpleStatementLine):
        return False
    if not isinstance(expression.body[0], libcst.Expr) or not hasattr(expression.body[0], "value"):
        return False
    s: str = check_and_get_attribute(expression.body[0].value, "value")
    if s is None:
        return False
    return (s.startswith('"""') and s.endswith('"""')) or (s.startswith("'''") and s.endswith("'''"))


def merge_code_strings(uncommented_code: str, commented_code: str) -> str:
    """
    Merge uncommented code from astor parser and commented code from ast_comments parser

    Args:
        uncommented_code: code without comments from astor parser
        commented_code: code with comments from ast_comments parser

    Returns:
        commented_code: but with updated line breaks
    """
    # Split the code strings into lines
    uncommented_lines = uncommented_code.split("\n")
    commented_lines = commented_code.split("\n")

    comment_counter = 0  # keep track of number of comments
    for line_uncommented, (j, _) in zip(uncommented_lines, enumerate(commented_lines)):
        if j + comment_counter == len(commented_lines):
            break  # reached the end of the commented code

        # iterate over an arbitrary number of comments and keep a count of them
        while commented_lines[j + comment_counter].strip().startswith("#"):
            comment_counter += 1

        # if come across a line break in the uncommented code
        # check that the equivalent position in commented code is a line break
        # if not, then insert a line break
        if line_uncommented == "":
            if commented_lines[j + comment_counter] != "":
                commented_lines.insert(j + comment_counter, "")

    # Join the lines and return the merged code
    return "\n".join(commented_lines)


def remove_comment_nodes(node: Any) -> Any:
    """
    Remove instances of ast_comments.Comment from the AST tree
    Args:
        node: current node in the tree

    Returns:
        node without comments
    """

    if hasattr(node, "body"):
        node.body = [remove_comment_nodes(n) for n in node.body if not isinstance(n, ast_comments.Comment)]
    return node


def create_path(path: str) -> None:
    if Path(path).suffix:
        path = Path(path).parent.as_posix()
    os.makedirs(path, exist_ok=True)
