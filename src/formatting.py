"""Reformat class method definitions"""
import ast
from typing import Dict
from typing import List
from typing import Optional

import astor

from src.configs import CLASS_SPACING
from src.functions import get_method_type_and_name
from src.functions import is_csortable
from src.utilities import extract_text_from_file


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
    if file_path:
        return astor.parse_file(file_path)
    if code:
        return ast.parse(code)
    raise ValueError("Must provide code or file_path!")


def find_classes(code: ast.Module) -> Dict[str, ast.ClassDef]:
    """
    Find all class definitions within parsed code
    Args:
        code: parsed code module

    Returns:
        classes: list of class definitions
    """
    classes = {}

    # Find all function definitions
    for node in code.body:
        if isinstance(node, ast.ClassDef):
            classes[node.name] = node

    # Sort the functions based on their line numbers
    # classes.sort(key=lambda x: x[0])
    return classes


def find_methods(code: ast.ClassDef) -> List[ast.stmt]:
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

    # Sort the functions based on their line numbers
    # functions.sort(key=lambda x: x[0])
    return functions


def order_class_functions(methods: List[ast.stmt]) -> List[ast.stmt]:
    """
    Sort a list of method definitions by the method type and alphabetically by method name
    Args:
        methods: list of method definitions

    Returns:
        sorted_methods: method definitions sorted by method type
    """
    sorted_methods = sorted(methods, key=get_method_type_and_name)
    return sorted_methods


def main(file_path: str, output_py: Optional[str] = None) -> None:
    output_py = file_path if output_py is None else output_py
    python_code = extract_text_from_file(file_path)
    parsed_code = parse_code(code=python_code, file_path=file_path)
    classes = find_classes(parsed_code)
    functions = {name: find_methods(cls) for name, cls in classes.items()}

    sorted_functions: Dict[str, List[ast.stmt]] = {
        cls: order_class_functions(methods) for cls, methods in functions.items()
    }

    for name, cls in classes.items():
        cls.body = sorted_functions[name]

    with open(output_py, "w", encoding="utf-8") as f:
        for _, code in classes.items():
            f.writelines(ast.unparse(code))
            f.writelines(CLASS_SPACING)
