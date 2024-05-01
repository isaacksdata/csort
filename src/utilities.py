import ast
from typing import Callable
from typing import Dict


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


def get_function_name(method: ast.FunctionDef) -> str:
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
    if not hasattr(attribute.target, "id"):
        raise AttributeError("ID attribute not found for attribute.target")
    return attribute.target.id


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
    if not hasattr(attribute.targets[0], "id"):
        raise AttributeError("ID attribute not found for attribute.targets")
    return attribute.targets[0].id


def get_ellipsis_name(expression: ast.Expr) -> str:
    """
    Extract name from an Ellipsis node
    Args:
        expression: ellipsis expression

    Returns:
        name
    """
    if not hasattr(expression.value, "value"):
        raise AttributeError("Could not find value attribute!")
    return str(expression.value.value)


names_factory: Dict[type, Callable] = {
    ast.FunctionDef: get_function_name,
    ast.AnnAssign: get_annotated_attribute_name,
    ast.Assign: get_attribute_name,
}


def get_expression_name(expression: ast.stmt) -> str:
    """
    Extract name from ast parsed expression

    Args:
        expression: ast parsed expression

    Returns:
        name of the expression
    """
    if is_ellipsis(expression) and isinstance(expression, ast.Expr):
        return get_ellipsis_name(expression)
    return names_factory[type(expression)](expression)


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
        return str(constant_value) == "Ellipsis"
    return False
