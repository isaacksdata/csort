import ast
import os

import pytest

from src.diff import SyntaxTreeDiffGenerator


DEBUG = "tests" in os.getcwd()


@pytest.fixture
def differ():
    return SyntaxTreeDiffGenerator()


@pytest.fixture
def input_script():
    if DEBUG:
        return "../scripts/basic_input.py"
    return "tests/scripts/basic_input.py"


@pytest.fixture
def expected_script():
    if DEBUG:
        return "../scripts/basic_expected.py"
    return "tests/scripts/basic_expected.py"


@pytest.fixture
def func_source_code():
    return "def func() -> int:\n    return 1"


@pytest.fixture
def static_func_source_code():
    return "@staticmethod\ndef static_func() -> int:\n    return 1"


@pytest.fixture
def private_func_source_code():
    return "def _private_func() -> int:\n    return 1"


def test_ast_diff_generator_init(differ):
    assert isinstance(differ._source_code_methods, list)
    assert isinstance(differ._modified_code_methods, list)


def test_ast_diff_generator_extract_method_names(
    differ, func_source_code, static_func_source_code, private_func_source_code
):
    methods = [
        ast.parse(private_func_source_code).body[0],
        ast.parse(static_func_source_code).body[0],
        ast.parse(func_source_code).body[0],
    ]
    output = differ._extract_method_names(methods)
    assert isinstance(output, list)
    assert output == ["_private_func", "static_func", "func"]


def test_ast_diff_generator_extract_method_names_typeerror(differ):
    methods = ["string", 4]
    with pytest.raises(TypeError):
        differ._extract_method_names(methods)


def test_ast_diff_generator_diff(differ, func_source_code, static_func_source_code, private_func_source_code):
    expected = "[0] : _private_func     --->     static_func\n[1] : static_func       --->     func\n[2] : func              --->     _private_func"
    methods = [
        ast.parse(private_func_source_code).body[0],
        ast.parse(static_func_source_code).body[0],
        ast.parse(func_source_code).body[0],
    ]
    ordered_methods = [methods[1], methods[2], methods[0]]
    output = differ.diff(methods, ordered_methods)
    assert isinstance(output, str)
    assert output == expected


def test_ast_diff_generator_diff_no_diff(differ, func_source_code, static_func_source_code, private_func_source_code):
    expected = "No changes made!"
    methods = [
        ast.parse(private_func_source_code).body[0],
        ast.parse(static_func_source_code).body[0],
        ast.parse(func_source_code).body[0],
    ]
    output = differ.diff(methods, methods)
    assert isinstance(output, str)
    assert output == expected
