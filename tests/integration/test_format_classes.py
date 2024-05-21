import importlib
import json
import logging
import os
import subprocess
from pathlib import Path

import ast_comments
import astor
import libcst
import pytest

from src.config_loader import ConfigLoader
from src.formatting import format_csort
from src.method_describers import get_method_describer
from src.utilities import extract_text_from_file

DEBUG = "tests" in os.getcwd()


@pytest.fixture
def input_path(request):
    if DEBUG:
        return f"../scripts/{request.param}_input.py"
    else:
        return f"./tests/scripts/{request.param}_input.py"


@pytest.fixture
def output_path(request):
    if DEBUG:
        return f"../scripts/{request.param}_output.py"
    else:
        return f"./tests/scripts/{request.param}_output.py"


@pytest.fixture
def expected_path(request):
    if DEBUG:
        return f"../scripts/{request.param}_expected.py"
    else:
        return f"./tests/scripts/{request.param}_expected.py"


@pytest.fixture
def parser(request):
    return importlib.import_module(f"src.{request.param}_functions")


@pytest.fixture
def method_describer(request):
    cfg = ConfigLoader(config_path=None).config
    return get_method_describer(parser_type=request.param, config=cfg)


def simple_test(
    parser,
    method_describer,
    input_path,
    output_path,
    expected_path,
    comments: bool = False,
    use_cst: bool = False,
    **kwargs,
):
    format_csort(
        parser=parser, file_path=input_path, output_py=output_path, method_describer=method_describer, **kwargs
    )
    if use_cst:
        code = libcst.parse_module(extract_text_from_file(output_path))
        expected_code = libcst.parse_module(extract_text_from_file(expected_path))
        assert code.code_for_node(code) == expected_code.code_for_node(expected_code)
    elif comments:
        code = ast_comments.parse(extract_text_from_file(output_path))
        expected_code = ast_comments.parse(extract_text_from_file(expected_path))
        assert ast_comments.unparse(code) == ast_comments.unparse(expected_code)
    else:
        code = astor.parse_file(output_path)
        expected_code = astor.parse_file(expected_path)
        assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["basic"], indirect=True)
@pytest.mark.parametrize("output_path", ["basic"], indirect=True)
@pytest.mark.parametrize("expected_path", ["basic"], indirect=True)
def test_formatting_ast(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["basic"], indirect=True)
@pytest.mark.parametrize("output_path", ["basic"], indirect=True)
@pytest.mark.parametrize("expected_path", ["basic"], indirect=True)
def test_formatting_cst(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["empty"], indirect=True)
@pytest.mark.parametrize("output_path", ["empty"], indirect=True)
@pytest.mark.parametrize("expected_path", ["empty"], indirect=True)
def test_formatting_empty_ast(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["empty"], indirect=True)
@pytest.mark.parametrize("output_path", ["empty"], indirect=True)
@pytest.mark.parametrize("expected_path", ["empty"], indirect=True)
def test_formatting_empty_cst(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["attributes"], indirect=True)
@pytest.mark.parametrize("output_path", ["attributes"], indirect=True)
@pytest.mark.parametrize("expected_path", ["attributes"], indirect=True)
def test_formatting_attributes_ast(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["attributes"], indirect=True)
@pytest.mark.parametrize("output_path", ["attributes"], indirect=True)
@pytest.mark.parametrize("expected_path", ["attributes"], indirect=True)
def test_formatting_attributes_cst(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["decorators"], indirect=True)
@pytest.mark.parametrize("output_path", ["decorators"], indirect=True)
@pytest.mark.parametrize("expected_path", ["decorators"], indirect=True)
def test_formatting_decorators_ast(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["decorators"], indirect=True)
@pytest.mark.parametrize("output_path", ["decorators"], indirect=True)
@pytest.mark.parametrize("expected_path", ["decorators"], indirect=True)
def test_formatting_decorators_cst(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["multi_decorators"], indirect=True)
@pytest.mark.parametrize("output_path", ["multi_decorators"], indirect=True)
@pytest.mark.parametrize("expected_path", ["multi_decorators"], indirect=True)
def test_formatting_mutli_decorators_ast(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["multi_decorators"], indirect=True)
@pytest.mark.parametrize("output_path", ["multi_decorators"], indirect=True)
@pytest.mark.parametrize("expected_path", ["multi_decorators"], indirect=True)
def test_formatting_mutli_decorators_cst(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["other_code"], indirect=True)
@pytest.mark.parametrize("output_path", ["other_code"], indirect=True)
@pytest.mark.parametrize("expected_path", ["other_code"], indirect=True)
def test_formatting_other_code_ast(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["other_code"], indirect=True)
@pytest.mark.parametrize("output_path", ["other_code"], indirect=True)
@pytest.mark.parametrize("expected_path", ["other_code"], indirect=True)
def test_formatting_other_code_cst(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["docstrings_comments"], indirect=True)
@pytest.mark.parametrize("output_path", ["docstrings_comments"], indirect=True)
@pytest.mark.parametrize("expected_path", ["docstrings_comments"], indirect=True)
def test_formatting_docs_comments_ast(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path, comments=True)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["docstrings_comments"], indirect=True)
@pytest.mark.parametrize("output_path", ["docstrings_comments"], indirect=True)
@pytest.mark.parametrize("expected_path", ["docstrings_comments"], indirect=True)
def test_formatting_docs_comments_cst(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path, comments=True)


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["csort_group"], indirect=True)
@pytest.mark.parametrize("output_path", ["csort_group"], indirect=True)
@pytest.mark.parametrize("expected_path", ["csort_group"], indirect=True)
def test_formatting_csort_group_ast(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["csort_group"], indirect=True)
@pytest.mark.parametrize("output_path", ["csort_group"], indirect=True)
@pytest.mark.parametrize("expected_path", ["csort_group"], indirect=True)
def test_formatting_csort_group_cst(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["imports"], indirect=True)
@pytest.mark.parametrize("output_path", ["imports"], indirect=True)
@pytest.mark.parametrize("expected_path", ["imports"], indirect=True)
def test_formatting_imports_ast(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["imports"], indirect=True)
@pytest.mark.parametrize("output_path", ["imports"], indirect=True)
@pytest.mark.parametrize("expected_path", ["imports"], indirect=True)
def test_formatting_imports_cst(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path)


def complex_test(parser, method_describer, input_path, output_path, expected_path):
    format_csort(parser=parser, file_path=input_path, output_py=output_path, method_describer=method_describer)
    code = ast_comments.parse(extract_text_from_file(output_path))
    expected_code = ast_comments.parse(extract_text_from_file(expected_path))
    assert ast_comments.unparse(code) == ast_comments.unparse(expected_code)

    process = subprocess.Popen(["python", input_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    assert not error
    with open("primes.json", "r") as f:
        input_data = json.load(f)

    process = subprocess.Popen(["python", output_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    assert not error
    with open("primes.json", "r") as f:
        output_data = json.load(f)

    assert input_data["primes"] == output_data["primes"]

    Path(output_path).unlink()
    Path("primes.json").unlink()


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["complex"], indirect=True)
@pytest.mark.parametrize("output_path", ["complex"], indirect=True)
@pytest.mark.parametrize("expected_path", ["complex"], indirect=True)
def test_formatting_complex_ast(parser, method_describer, input_path, output_path, expected_path):
    complex_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["complex"], indirect=True)
@pytest.mark.parametrize("output_path", ["complex"], indirect=True)
@pytest.mark.parametrize("expected_path", ["complex"], indirect=True)
def test_formatting_complex_cst(parser, method_describer, input_path, output_path, expected_path):
    complex_test(parser, method_describer, input_path, output_path, expected_path)


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["pandas"], indirect=True)
@pytest.mark.parametrize("output_path", ["pandas"], indirect=True)
@pytest.mark.parametrize("expected_path", ["pandas"], indirect=True)
def test_formatting_pandas_ast(parser, method_describer, input_path, output_path, expected_path):
    # expect this to fail due to quote change by AST
    with pytest.raises(AssertionError):
        simple_test(parser, method_describer, input_path, output_path, expected_path, use_cst=True)


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["pandas"], indirect=True)
@pytest.mark.parametrize("output_path", ["pandas"], indirect=True)
@pytest.mark.parametrize("expected_path", ["pandas"], indirect=True)
def test_formatting_pandas_cst(parser, method_describer, input_path, output_path, expected_path):
    simple_test(parser, method_describer, input_path, output_path, expected_path, use_cst=True)


@pytest.mark.parametrize("parser", ["ast"], indirect=True)
@pytest.mark.parametrize("method_describer", ["ast"], indirect=True)
@pytest.mark.parametrize("input_path", ["auto_static"], indirect=True)
@pytest.mark.parametrize("output_path", ["auto_static"], indirect=True)
@pytest.mark.parametrize("expected_path", ["auto_static"], indirect=True)
def test_formatting_auto_static_ast(parser, method_describer, input_path, output_path, expected_path, caplog):
    caplog.set_level(logging.INFO)
    simple_test(parser, method_describer, input_path, output_path, expected_path, auto_static=True)
    assert "Csort converted 1 methods from MyClass to static!" in caplog.messages


@pytest.mark.parametrize("parser", ["cst"], indirect=True)
@pytest.mark.parametrize("method_describer", ["cst"], indirect=True)
@pytest.mark.parametrize("input_path", ["auto_static"], indirect=True)
@pytest.mark.parametrize("output_path", ["auto_static"], indirect=True)
@pytest.mark.parametrize("expected_path", ["auto_static"], indirect=True)
def test_formatting_auto_static_cst(parser, method_describer, input_path, output_path, expected_path, caplog):
    caplog.set_level(logging.INFO)
    simple_test(parser, method_describer, input_path, output_path, expected_path, use_cst=True, auto_static=True)
    assert "Csort converted 1 methods from MyClass to static!" in caplog.messages
