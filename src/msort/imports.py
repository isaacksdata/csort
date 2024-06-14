from typing import Union

import libcst


def is_import_libcst(node: libcst.CSTNode) -> bool:
    """
    Determine if a libcst node represents an import statement

    libcst has different node classes for different styles of import

    - import libcst --> libcst.Import
    - import libcst as l --> libcst.ImportAlias
    - from libcst import * --> libcst.ImportStar
    - from libcst import CSTNode --> libcst.ImportFrom

    Args:
        node: the libcst node to evaluate

    Returns:
        True if the node represents an import
    """
    if not isinstance(node, libcst.SimpleStatementLine):
        return False
    return isinstance(node.body[0], (libcst.Import, libcst.ImportFrom, libcst.ImportStar, libcst.ImportAlias))


def is_import_string(node: str) -> bool:
    """
    Determine if a string of code represents an import statement.

    The string is converted to a libcst node and then is_import_libcst can be called.

    Args:
        node: string of code to evaluate

    Returns:
        True if the string of code represents an import statement
    """
    try:
        lib_node = libcst.parse_statement(node)
    except libcst._exceptions.ParserSyntaxError:
        return False
    return is_import_libcst(lib_node)


def is_import(node: Union[libcst.CSTNode, str]) -> bool:
    """
    Determine if the input node represents an import statement
    Args:
        node: code to evaluate

    Returns:
        True if code represents an import statement
    """
    if isinstance(node, libcst.CSTNode):
        return is_import_libcst(node)
    return is_import_string(node)


def handle_import_formatting(source_code: str, ast_code: str) -> str:
    """
    Replace ast imports with libcst imports

    Ast parsing does not preserve spaces between import groups. the libcst library is used to parse the import
    statements with spacing preserved.

    The ast imports are removed and replaced with the libcst parsed imports.

    Args:
        source_code: original source code
        ast_code: ast parsed code

    Returns:
        new_code: ast code but with libcst parsed imports
    """
    lib_tree = libcst.parse_module(source_code)
    ast_code_list = ast_code.splitlines()
    import_statements = [i for i in lib_tree.body if is_import(i)]
    if len(import_statements) > 0:
        lib_import_code = "".join([lib_tree.code_for_node(node) for node in import_statements]).splitlines()
        ast_import_idx = [i for i, l in enumerate(ast_code_list) if is_import(l)]
        new_code = [*ast_code_list[: min(ast_import_idx)], *lib_import_code, *ast_code_list[max(ast_import_idx) + 1 :]]
        return "\n".join(new_code)
    return ast_code
