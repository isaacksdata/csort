import argparse
import logging
import os
import shutil
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from csort.main import main
from csort.main import parse_commandline
from csort.main import validate_paths


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


@pytest.fixture
def ini_config_path():
    if DEBUG:
        return "../unit/csort.ini"
    return "tests/unit/csort.ini"


@pytest.fixture
def toml_config_path():
    if DEBUG:
        return "../unit/pyproject_test.toml"
    return "tests/unit/pyproject_test.toml"


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
        output, args = parse_commandline()
    assert isinstance(output, argparse.Namespace)
    assert output.input_path == "test/input/path/file.py"
    assert output.output_path == "test/output/path/file.py"
    assert output.config_path == "test/config/csort.ini"
    assert output.skip_patterns == ["expected", "pattern"]
    assert output.parser == "cst"
    assert output.check
    assert len(args) == 0


def test_parse_commandline_files():
    commands = ["", "file1.py", "file2.py"]  # mock script name
    with patch.object(sys, "argv", commands):
        output, args = parse_commandline()
    assert isinstance(output, argparse.Namespace)
    assert len(output.files) == 2
    assert "file1.py" in output.files


def test_validate_paths(script_path, output_path):
    inputs, outputs = validate_paths(files=[], input_path=script_path, output_path=output_path)
    assert isinstance(inputs, list)
    assert isinstance(outputs, list)
    assert len(inputs) == len(outputs) == 1
    assert inputs[0] == script_path
    assert outputs[0] == output_path


def test_validate_paths_input_dir_output_file(script_path, output_path):
    script_path = Path(script_path).parent.as_posix()
    with pytest.raises(ValueError):
        validate_paths(files=[], input_path=script_path, output_path=output_path)


def test_validate_paths_input_dir_output_dir(script_path, output_path):
    script_path = Path(script_path).parent.as_posix()
    output_path = Path(output_path).parent.as_posix()
    inputs, outputs = validate_paths(files=[], input_path=script_path, output_path=output_path)
    assert isinstance(inputs, list)
    assert isinstance(outputs, list)
    assert len(inputs) == len(outputs)
    assert all(Path(i).stem == Path(o).stem for i, o in zip(inputs, outputs))


def test_validate_paths_input_file_output_dir(script_path, output_path):
    output_path = Path(output_path).parent.as_posix()
    inputs, outputs = validate_paths(files=[], input_path=script_path, output_path=output_path)
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
        validate_paths(files=[], input_path=input_path)


def test_main_no_scripts(caplog):
    os.makedirs("empty_dir", exist_ok=True)
    commands = ["", "--input-path=./empty_dir"]  # mock script name
    with patch.object(sys, "argv", commands):
        main()
    assert "No Python scripts found in ./empty_dir" in caplog.messages
    shutil.rmtree("./empty_dir")


def test_validate_paths_with_files(script_path, caplog):
    caplog.set_level(logging.INFO)
    inputs, outputs = validate_paths(files=[script_path])
    assert inputs == outputs == [script_path]
    assert f"Found 1 files as positional args: ['{script_path}']" in caplog.messages


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


def test_main_ast(script_path, output_path, caplog):
    caplog.set_level(logging.DEBUG)
    commands = [
        "",
        f"--input-path={script_path}",
        f"--output-path={output_path}",
        "--parser=ast",
    ]  # mock script name as first arg
    with patch.object(sys, "argv", commands):
        main()
    assert Path(output_path).exists()
    assert f"Reformatting {script_path} ..." in caplog.messages
    assert "Using the AST parser!" in caplog.messages
    shutil.rmtree(Path(output_path).parent.as_posix())


def test_main_check_unchanged(script_path, caplog):
    caplog.set_level(logging.INFO)
    script_path = script_path.replace("_input", "_expected")
    commands = ["", f"--input-path={script_path}", f"--output-path={output_path}", "--check", "--n-auto-static"]
    with patch.object(sys, "argv", commands):
        main()
    assert "No changes made!" in caplog.messages
    assert any("Csort ran in check mode : 0 / 1 files would be changed!" in msg for msg in caplog.messages)


def test_main_check(script_path, caplog):
    caplog.set_level(logging.INFO)
    commands = ["", f"--input-path={script_path}", f"--output-path={output_path}", "--check"]
    with patch.object(sys, "argv", commands):
        main()
    assert "No changes made!" not in caplog.messages
    assert any("Csort ran in check mode : 1 / 1 files would be changed!" in msg for msg in caplog.messages)


def test_main_check_skip_pattern(script_path, caplog):
    caplog.set_level(logging.DEBUG)
    commands = ["", f"--input-path={script_path}", f"--output-path={output_path}", "--skip-patterns", "basic"]
    with patch.object(sys, "argv", commands):
        main()
    assert f"Skipping {script_path}" in caplog.messages


def test_main_check_diff(script_path, caplog):
    caplog.set_level(logging.INFO)
    commands = ["", f"--input-path={script_path}", f"--output-path={output_path}", "--diff"]
    with patch.object(sys, "argv", commands):
        main()
    assert any("Csort ran in diff mode" in msg for msg in caplog.messages)
    assert any("func                --->     __len__" in msg for msg in caplog.messages)


def test_main_check_order_override(script_path, caplog):
    caplog.set_level(logging.INFO)
    commands = [
        "",
        f"--input-path={script_path}",
        f"--output-path={output_path}",
        "--diff",
        "--n-auto-static",
        "--private-method=3",
        "--dunder-method=12",
    ]
    with patch.object(sys, "argv", commands):
        main()
    assert "Overriding dunder_method order : set to 12" in caplog.messages
    assert "Overriding private_method order : set to 3" in caplog.messages
    assert any("__init__            --->     _func" in msg for msg in caplog.messages)


def test_main_check_order_override_same_value(script_path, caplog):
    caplog.set_level(logging.INFO)
    commands = [
        "",
        f"--input-path={script_path}",
        f"--output-path={output_path}",
        "--diff",
        "--n-auto-static",
        "--private-method=3",
        "--dunder-method=3",
    ]
    with patch.object(sys, "argv", commands):
        main()
    assert "Overriding dunder_method order : set to 3" in caplog.messages
    assert "Overriding private_method order : set to 3" in caplog.messages
    assert any(
        "[0] : __init__            --->     __init__\n[1] : func                --->     __len__\n[2] : _func" in msg
        for msg in caplog.messages
    )


def test_main_ini_config(script_path, output_path, ini_config_path, caplog):
    caplog.set_level(logging.DEBUG)
    commands = [
        "",
        f"--input-path={script_path}",
        f"--output-path={output_path}",
        f"--config-path={ini_config_path}",
    ]  # mock script name as first arg
    with patch.object(sys, "argv", commands):
        main()
    assert Path(output_path).exists()
    assert f"Reformatting {script_path} ..." in caplog.messages
    assert f"Loading csort configurations from {ini_config_path}" in caplog.messages
    shutil.rmtree(Path(output_path).parent.as_posix())


def test_main_toml_config(script_path, output_path, toml_config_path, caplog):
    caplog.set_level(logging.DEBUG)
    commands = [
        "",
        f"--input-path={script_path}",
        f"--output-path={output_path}",
        f"--config-path={toml_config_path}",
    ]  # mock script name as first arg
    with patch.object(sys, "argv", commands):
        main()
    assert Path(output_path).exists()
    assert f"Reformatting {script_path} ..." in caplog.messages
    assert f"Loading csort configurations from {toml_config_path}" in caplog.messages
    shutil.rmtree(Path(output_path).parent.as_posix())
