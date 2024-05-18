import argparse
import logging
import os
import shutil
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from src.main import main
from src.main import parse_commandline
from src.main import validate_paths


DEBUG = "tests" in os.getcwd()


@pytest.fixture
def script_path():
    if DEBUG:
        return "../scripts/basic_input.py"
    return "tests/scripts/basic_input.py"


@pytest.fixture
def output_path():
    if DEBUG:
        return "../scripts/output/basic_output.py"
    return "tests/scripts/output/basic_output.py"


def test_parse_commandline():
    commands = [
        "",  # mock script name
        "--input-path=test/input/path/file.py",
        "--output-path=test/output/path/file.py",
        "--config-path=test/config/csort.ini",
        "--skip-patterns=expected",
        "--skip-patterns=pattern",
        "--parser=cst",
        "--check",
    ]
    with patch.object(sys, "argv", commands):
        output = parse_commandline()
    assert isinstance(output, argparse.Namespace)
    assert output.input_path == "test/input/path/file.py"
    assert output.output_path == "test/output/path/file.py"
    assert output.config_path == "test/config/csort.ini"
    assert output.skip_patterns == ["expected", "pattern"]
    assert output.parser == "cst"
    assert output.check


def test_validate_paths(script_path, output_path):
    inputs, outputs = validate_paths(script_path, output_path)
    assert isinstance(inputs, list)
    assert isinstance(outputs, list)
    assert len(inputs) == len(outputs) == 1
    assert inputs[0] == script_path
    assert outputs[0] == output_path


def test_validate_paths_input_dir_output_file(script_path, output_path):
    script_path = Path(script_path).parent.as_posix()
    with pytest.raises(ValueError):
        validate_paths(script_path, output_path)


def test_validate_paths_input_dir_output_dir(script_path, output_path):
    script_path = Path(script_path).parent.as_posix()
    output_path = Path(output_path).parent.as_posix()
    inputs, outputs = validate_paths(script_path, output_path)
    assert isinstance(inputs, list)
    assert isinstance(outputs, list)
    assert len(inputs) == len(outputs)
    assert all(Path(i).stem == Path(o).stem for i, o in zip(inputs, outputs))


def test_validate_paths_input_file_output_dir(script_path, output_path):
    output_path = Path(output_path).parent.as_posix()
    inputs, outputs = validate_paths(script_path, output_path)
    assert isinstance(inputs, list)
    assert isinstance(outputs, list)
    assert len(inputs) == len(outputs)
    assert (
        outputs[0]
        == Path(script_path).parent.joinpath(Path(output_path).stem).joinpath(Path(script_path).name).as_posix()
    )


def test_validate_paths_not_exist():
    input_path = "input/script.py"
    with pytest.raises(FileNotFoundError):
        validate_paths(input_path)


def test_main_no_scripts(caplog):
    os.makedirs("empty_dir", exist_ok=True)
    commands = ["", "--input-path=./empty_dir"]  # mock script name
    with patch.object(sys, "argv", commands):
        main()
    assert "No Python scripts found in ./empty_dir" in caplog.messages
    shutil.rmtree("./empty_dir")


def test_main(script_path, output_path, caplog):
    caplog.set_level(logging.DEBUG)
    commands = ["", f"--input-path={script_path}", f"--output-path={output_path}"]  # mock script name as first arg
    with patch.object(sys, "argv", commands):
        main()
    assert Path(output_path).exists()
    assert f"Reformatting {script_path} ..." in caplog.messages
    shutil.rmtree(Path(output_path).parent.as_posix())


def test_main_cst(script_path, output_path, caplog):
    caplog.set_level(logging.DEBUG)
    commands = [
        "",
        f"--input-path={script_path}",
        f"--output-path={output_path}",
        "--parser=cst",
    ]  # mock script name as first arg
    with patch.object(sys, "argv", commands):
        main()
    assert Path(output_path).exists()
    assert f"Reformatting {script_path} ..." in caplog.messages
    assert "Using the CST parser!" in caplog.messages
    shutil.rmtree(Path(output_path).parent.as_posix())


def test_main_check_unchanged(script_path, caplog):
    script_path = script_path.replace("_input", "_expected")
    commands = ["", f"--input-path={script_path}", f"--output-path={output_path}", "--check"]
    with patch.object(sys, "argv", commands):
        main()
