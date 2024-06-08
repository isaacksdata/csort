"""
Module for functions handling specific edge cases
"""
import re
from typing import Callable
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


handlers: List[Callable] = [handle_if_name_main, handle_last_line_white_space, handle_decorator_spaces]


def handle_edge_cases(source_code: str) -> str:
    """
    Check for and correct specific edge cases defined in handlers
    Args:
        source_code: input source code

    Returns:
        source code: after edge case handling
    """
    for handler in handlers:
        source_code = handler(source_code)
    return source_code
