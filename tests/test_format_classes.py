import os
from pathlib import Path

import astor
import pytest

from src.formatting import main


@pytest.fixture
def input_path(request):
    if os.getcwd().endswith("tests"):
        return f"./scripts/{request.param}_input.py"
    else:
        return f"./tests/scripts/{request.param}_input.py"


@pytest.fixture
def output_path(request):
    if os.getcwd().endswith("tests"):
        return f"./scripts/{request.param}_output.py"
    else:
        return f"./tests/scripts/{request.param}_output.py"


@pytest.fixture
def expected_path(request):
    if os.getcwd().endswith("tests"):
        return f"./scripts/{request.param}_expected.py"
    else:
        return f"./tests/scripts/{request.param}_expected.py"


@pytest.mark.parametrize("input_path", ["basic"], indirect=True)
@pytest.mark.parametrize("output_path", ["basic"], indirect=True)
@pytest.mark.parametrize("expected_path", ["basic"], indirect=True)
def test_formatting(input_path, output_path, expected_path):
    main(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["empty"], indirect=True)
@pytest.mark.parametrize("output_path", ["empty"], indirect=True)
@pytest.mark.parametrize("expected_path", ["empty"], indirect=True)
def test_formatting_empty(input_path, output_path, expected_path):
    main(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["attributes"], indirect=True)
@pytest.mark.parametrize("output_path", ["attributes"], indirect=True)
@pytest.mark.parametrize("expected_path", ["attributes"], indirect=True)
def test_formatting_attributes(input_path, output_path, expected_path):
    main(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["decorators"], indirect=True)
@pytest.mark.parametrize("output_path", ["decorators"], indirect=True)
@pytest.mark.parametrize("expected_path", ["decorators"], indirect=True)
def test_formatting_decorators(input_path, output_path, expected_path):
    main(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()


@pytest.mark.parametrize("input_path", ["other_code"], indirect=True)
@pytest.mark.parametrize("output_path", ["other_code"], indirect=True)
@pytest.mark.parametrize("expected_path", ["other_code"], indirect=True)
def test_formatting_decorators(input_path, output_path, expected_path):
    main(input_path, output_py=output_path)
    code = astor.parse_file(output_path)
    expected_code = astor.parse_file(expected_path)
    assert astor.to_source(code) == astor.to_source(expected_code)
    Path(output_path).unlink()
