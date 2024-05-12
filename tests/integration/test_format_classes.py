import json
import os
import subprocess
from pathlib import Path

import ast_comments
import astor
import pytest

from src.formatting import format_csort
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


@pytest.mark.parametrize("input_path", ["basic"], indirect=True)
@pytest.mark.parametrize("output_path", ["basic"], indirect=True)
@pytest.mark.parametrize("expected_path", ["basic"], indirect=True)
def test_formatting(input_path, output_path, expected_path):
    format_csort(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["empty"], indirect=True)
@pytest.mark.parametrize("output_path", ["empty"], indirect=True)
@pytest.mark.parametrize("expected_path", ["empty"], indirect=True)
def test_formatting_empty(input_path, output_path, expected_path):
    format_csort(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["attributes"], indirect=True)
@pytest.mark.parametrize("output_path", ["attributes"], indirect=True)
@pytest.mark.parametrize("expected_path", ["attributes"], indirect=True)
def test_formatting_attributes(input_path, output_path, expected_path):
    format_csort(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["decorators"], indirect=True)
@pytest.mark.parametrize("output_path", ["decorators"], indirect=True)
@pytest.mark.parametrize("expected_path", ["decorators"], indirect=True)
def test_formatting_decorators(input_path, output_path, expected_path):
    format_csort(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["multi_decorators"], indirect=True)
@pytest.mark.parametrize("output_path", ["multi_decorators"], indirect=True)
@pytest.mark.parametrize("expected_path", ["multi_decorators"], indirect=True)
def test_formatting_mutli_decorators(input_path, output_path, expected_path):
    format_csort(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["other_code"], indirect=True)
@pytest.mark.parametrize("output_path", ["other_code"], indirect=True)
@pytest.mark.parametrize("expected_path", ["other_code"], indirect=True)
def test_formatting_other_code(input_path, output_path, expected_path):
    format_csort(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["docstrings_comments"], indirect=True)
@pytest.mark.parametrize("output_path", ["docstrings_comments"], indirect=True)
@pytest.mark.parametrize("expected_path", ["docstrings_comments"], indirect=True)
def test_formatting_docs_comments(input_path, output_path, expected_path):
    format_csort(input_path, output_py=output_path)
    code = ast_comments.parse(extract_text_from_file(output_path))
    expected_code = ast_comments.parse(extract_text_from_file(expected_path))
    assert ast_comments.unparse(code) == ast_comments.unparse(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["csort_group"], indirect=True)
@pytest.mark.parametrize("output_path", ["csort_group"], indirect=True)
@pytest.mark.parametrize("expected_path", ["csort_group"], indirect=True)
def test_formatting_csort_group(input_path, output_path, expected_path):
    format_csort(input_path, output_py=output_path)
    code = ast_comments.parse(extract_text_from_file(output_path))
    expected_code = ast_comments.parse(extract_text_from_file(expected_path))
    assert ast_comments.unparse(code) == ast_comments.unparse(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["imports"], indirect=True)
@pytest.mark.parametrize("output_path", ["imports"], indirect=True)
@pytest.mark.parametrize("expected_path", ["imports"], indirect=True)
def test_formatting_imports(input_path, output_path, expected_path):
    format_csort(input_path, output_py=output_path)
    code = ast_comments.parse(extract_text_from_file(output_path))
    expected_code = ast_comments.parse(extract_text_from_file(expected_path))
    assert ast_comments.unparse(code) == ast_comments.unparse(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["complex"], indirect=True)
@pytest.mark.parametrize("output_path", ["complex"], indirect=True)
@pytest.mark.parametrize("expected_path", ["complex"], indirect=True)
def test_formatting_complex(input_path, output_path, expected_path):
    format_csort(input_path, output_py=output_path)
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
