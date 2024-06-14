"""
Module for functions handling specific edge cases
"""
import re
from typing import Callable
from typing import Dict
from typing import List


def handle_if_name_main(source_code: str) -> str:
    """
    Ensure that there are two clear lines immediately before "if __name__ == '__main__'"
    Args:
        source_code: unparsed code

    Returns:
        source_code: after checking edgecase
    """
    pattern = "if __name__ == '__main__'"
    reg = f"(?:\n*){pattern}"
    replacement = f"\n\n\n{pattern}"
    if pattern in source_code:
        source_code = re.sub(reg, replacement, source_code)
    return source_code


def handle_last_line_white_space(source_code: str) -> str:
    """
    Add a blank line at end of file if not present
    Args:
        source_code: source code as a string

    Returns:
        source_code: with blank final line
    """
    if not source_code.endswith("\n"):
        source_code = source_code + "\n"
    return source_code


def handle_decorator_spaces(source_code: str) -> str:
    """
    Remove empty lines between decorator and function definition
    Args:
        source_code: source code string

    Returns:
        source_code without empty lines
    """
    lines = source_code.splitlines()
    lines_to_drop = [i + 1 for i, l in enumerate(lines) if l.strip().startswith("@") and lines[i + 1] == ""]
    lines = [l for i, l in enumerate(lines) if i not in lines_to_drop]
    return "\n".join(lines)


def handle_empty_line_between_class_methods(source_code: str) -> str:
    """
    Ensure that class functions are separated with blank line from end of preceding component
    Args:
        source_code: source code as a string

    Returns:
        source code with additional blank lines
    """
    idx = []
    lines = source_code.splitlines()
    accept_patterns = ["@", "class"]
    for i, line in enumerate(lines):
        # if a line begins with @ then its a decorator and check to make sure line beforehand is decorator blank
        if (
            line.strip().startswith("@")
            and not any(lines[i - 1].strip().startswith(p) for p in accept_patterns)
            and lines[i - 1] != ""
        ):
            idx.append(i)
        # if a line begins with def then preceding line should be a decorator or blank
        elif (
            line.strip().startswith("def ")
            and not any(lines[i - 1].strip().startswith(p) for p in accept_patterns)
            and lines[i - 1] != ""
        ):
            idx.append(i)
        else:
            pass
    for i, j in enumerate(idx):
        lines.insert(i + j, "")
    return "\n".join(lines)


def handle_empty_lines_after_class_definition(source_code: str) -> str:
    """
    Remove empty lines after class definitions

    E.g.
    class MyClass:

        def func(self):
            pass

    -->

    class MyClass:
        def func(self):
            pass

    Args:
        source_code: source code string

    Returns:
        source code without blank lines after class definitions
    """
    idx = []
    lines = source_code.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("class") and lines[i + 1] == "":
            idx.append(i + 1)
    lines = [l for i, l in enumerate(lines) if i not in idx]
    return "\n".join(lines)


handlers: Dict[str, List[Callable]] = {
    "ast": [
        handle_if_name_main,
        handle_decorator_spaces,
        handle_empty_lines_after_class_definition,
        handle_last_line_white_space,
    ],
    "cst": [
        handle_empty_line_between_class_methods,
        handle_empty_lines_after_class_definition,
        handle_last_line_white_space,
    ],
}


def handle_edge_cases(source_code: str, parser: str) -> str:
    """
    Check for and correct specific edge cases defined in handlers
    Args:
        source_code: input source code
        parser: type of parser being used - edge cases are parser dependent

    Returns:
        source code: after edge case handling
    """
    for handler in handlers[parser]:
        source_code = handler(source_code)
    return source_code
