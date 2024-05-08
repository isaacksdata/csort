"""Reformat class method definitions"""
import ast
from copy import deepcopy
from typing import Dict
from typing import List
from typing import Optional
from typing import TypedDict

import ast_comments
import astor

from src.config_loader import ConfigLoader
from src.edge_cases import handle_edge_cases
from src.functions import ASTMethodDescriber
from src.functions import describe_method
from src.functions import is_csortable
from src.imports import handle_import_formatting
from src.utilities import extract_text_from_file
from src.utilities import merge_code_strings
from src.utilities import remove_comment_nodes


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
        return ast_comments.parse(code)
    raise ValueError("Must provide code or file_path!")


find_classes_response = TypedDict("find_classes_response", {"node": ast.ClassDef, "index": int})


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
        if isinstance(node, ast.ClassDef):
            classes[node.name] = find_classes_response(node=node, index=i)

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


def order_class_functions(methods: List[ast.stmt], method_describer: ASTMethodDescriber) -> List[ast.stmt]:
    """
    Sort a list of method definitions by the method type and alphabetically by method name
    Args:
        methods: list of method definitions
        method_describer: instance of MethodDescriber for classifying methods of classes

    Returns:
        sorted_methods: method definitions sorted by method type
    """
    sorted_methods = sorted(methods, key=lambda m: describe_method(method=m, method_describer=method_describer))
    return sorted_methods


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


def main(file_path: str, output_py: Optional[str] = None) -> None:
    # get config file
    config_loader = ConfigLoader()
    cfg = config_loader.config

    # build method describer
    method_describer = ASTMethodDescriber(config=cfg)

    output_py = file_path if output_py is None else output_py
    python_code = extract_text_from_file(file_path)
    parsed_code = parse_code(code=python_code, file_path=file_path)
    parsed_code = parse_code(code=python_code)
    classes = find_classes(parsed_code)
    functions = {name: find_methods(cls["node"]) for name, cls in classes.items()}

    sorted_functions: Dict[str, List[ast.stmt]] = {
        cls: order_class_functions(methods, method_describer) for cls, methods in functions.items()
    }

    # update the classes dictionary with new class body
    for name, cls in classes.items():
        cls["node"].body = sorted_functions[name]

    # update parsed code with sorted classes
    for _, cls in classes.items():
        parsed_code.body[cls["index"]] = cls["node"]

    # unparse code and add extra line space between classes
    new_code = preserve_comments(parsed_code)

    new_code = handle_edge_cases(new_code)

    new_code = handle_import_formatting(source_code=python_code, ast_code=new_code)

    with open(output_py, "w", encoding="utf-8") as f:
        f.writelines(new_code)
