"""Reformat class method definitions"""
import ast
import logging
from types import ModuleType
from typing import Dict
from typing import List
from typing import Optional

from src.configs import format_csort_response
from src.decorators import StaticMethodChecker
from src.diff import SyntaxTreeDiffGenerator
from src.method_describers import describe_method
from src.method_describers import MethodDescriber
from src.utilities import create_path
from src.utilities import extract_text_from_file


def order_class_functions(methods: List[ast.stmt], method_describer: MethodDescriber) -> List[ast.stmt]:
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


def format_csort(
    parser: ModuleType,
    file_path: str,
    method_describer: MethodDescriber,
    output_py: Optional[str] = None,
    auto_static: bool = False,
) -> format_csort_response:
    """
    Main function for running Csort
    Args:
        parser: Module containing functions for specified code parser
        file_path: path to source code (.py) file
        method_describer: instance of MethodDescriber for extracting class method info
        output_py: where to write out formatted code (.py) file
        auto_static: If True, then static methods without the @staticmethod decorator will be marked as static

    Returns:
        {
            "code" : indicates whether file has changed or not
            "diff": string indicating changes introduced by csort
        }
    """

    python_code = extract_text_from_file(file_path)
    parsed_code = parser.parse_code(code=python_code, file_path=file_path)
    classes = parser.find_classes(parsed_code)
    functions = {name: parser.extract_class_components(cls["node"]) for name, cls in classes.items()}

    if auto_static:
        static_checker = StaticMethodChecker()
        functions = static_checker.staticise_classes(functions)
        for class_name, n_changes in static_checker.class_static_method_counts.items():
            if n_changes > 0:
                logging.info("Csort converted %s methods from %s to static!", n_changes, class_name)

    sorted_functions: Dict[str, List[ast.stmt]] = {
        cls: order_class_functions(methods, method_describer) for cls, methods in functions.items()
    }

    if all(functions[cname] == sorted_functions[cname] for cname in functions.keys()):
        logging.info("No changes made!")
        return format_csort_response(code=0, diff="")
    # update the classes dictionary with new class body
    classes = {name: parser.update_node(cls, sorted_functions[name]) for name, cls in classes.items()}
    # update parsed code with sorted classes
    parsed_code = parser.update_module(parsed_code, classes)

    new_code = parser.nodes_to_code(tree=parsed_code, source_code=python_code)

    diff_gen = SyntaxTreeDiffGenerator()
    diff_list = []
    for cls_name in functions:
        diff = diff_gen.diff(functions[cls_name], sorted_functions[cls_name])
        diff = f"**************\n ***** {file_path} *****\n**************\n" + f"\n ----- {cls_name} ----- \n" + diff
        diff_list.append(diff)
    compiled_diff = "/n/n".join(diff_list)

    if output_py is not None:
        create_path(output_py)
        with open(output_py, "w", encoding="utf-8") as f:
            f.writelines(new_code)
    return format_csort_response(code=1, diff=compiled_diff)
