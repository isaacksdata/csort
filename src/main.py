"""
Command line entrypoint for Csort
"""
import argparse
import logging
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

from src.formatting import format_csort


def parse_commandline() -> argparse.Namespace:
    """Parse CLI arguments using argparse"""
    parser = argparse.ArgumentParser(
        description="Takes as input the path to .py file or directory containing .py files and re-orders methods of "
        "classes according to Csort guidelines."
    )
    parser.add_argument(
        "-ip",
        "--input-path",
        type=str,
        default="./",
        help="Relative filepath to python source code files",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        type=str,
        default=None,
        help="Relative filepath to where formatted source should be saved. If None, then original files will be "
        "modified.",
    )
    parser.add_argument(
        "-cp",
        "--config-path",
        type=str,
        default=None,
        help="Relative filepath to a csort.ini file.",
    )
    parser.add_argument(
        "-sp",
        "--skip-patterns",
        action="append",
        help="Provide patterns to look for in .py file and avoid running csort on these scripts.",
    )
    params = parser.parse_args()

    return params


def _validate_paths_input_file(input_path: Path, output_path: Optional[Path] = None) -> Tuple[List[str], List[str]]:
    """
    Validate that the input file path and output path are compatible when the user has specified a specific input file
    Args:
        input_path: file path to a .py file
        output_path: output path to a file or directory

    Returns:
        py_scripts: list of paths to .py scripts for formatting
        outputs: list of paths where formatted scripts will be written to
    """
    py_scripts = [input_path.as_posix()]
    if output_path is None:
        outputs = [input_path.as_posix()]
    elif output_path.as_posix().endswith(".py"):
        outputs = [output_path.as_posix()]
    else:
        logging.info("Treating output path %s as a directory!", output_path.as_posix())
        outputs = [output_path.joinpath(input_path.name).as_posix()]
    return py_scripts, outputs


def _validate_paths_input_dir(input_path: Path, output_path: Optional[Path] = None) -> Tuple[List[str], List[str]]:
    """
    Validate that the input file path and output path are compatible when the user has specified an input directory
    Args:
        input_path: file path to a a directory containing .py files
        output_path: output path to a file or directory

    Returns:
        py_scripts: list of paths to .py scripts for formatting
        outputs: list of paths where formatted scripts will be written to
    """
    py_scripts = [script.as_posix() for script in input_path.rglob(pattern="*.py")]
    if output_path is None:
        outputs = py_scripts
    elif output_path.as_posix().endswith(".py"):
        raise ValueError("Input path is a directory but output path is a .py file!")
    else:
        logging.info("Treating output path %s as a directory!", output_path.as_posix())
        outputs = [output_path.joinpath(Path(script).name).as_posix() for script in py_scripts]
    return py_scripts, outputs


def validate_paths(input_path: str, output_path: Optional[str] = None) -> Tuple[List[str], List[str]]:
    """
    Validate that the user provided input and output paths are compatible.

    Args:
        input_path: file path to input script or directory of scripts
        output_path: path to output script or output directory

    Returns:
        py_scripts: list of paths to .py scripts for formatting
        outputs: list of paths where formatted scripts will be written to
    """
    input_pure_path = Path(input_path)
    output_pure_path = Path(output_path) if output_path is not None else None

    if not input_pure_path.exists():
        raise FileNotFoundError("Input path does not exist!")

    if input_pure_path.is_file():
        py_scripts, outputs = _validate_paths_input_file(input_pure_path, output_pure_path)
    elif input_pure_path.is_dir():
        py_scripts, outputs = _validate_paths_input_dir(input_pure_path, output_pure_path)
    else:
        raise ValueError("Input path is neither a file or a directory! ")
    return py_scripts, outputs


def main() -> None:
    params = parse_commandline()
    skip_patterns = [] if params.skip_patterns is None else params.skip_patterns

    py_scripts, outputs = validate_paths(input_path=params.input_path, output_path=params.output_path)

    if len(py_scripts) == 0:
        logging.warning("No Python scripts found in %s", params.input_path)

    for input_script, output_script in zip(py_scripts, outputs):
        if any(skip_pat in Path(input_script).stem for skip_pat in skip_patterns):
            logging.debug("Skipping %s", input_script)
            continue
        logging.debug("Reformatting %s ...", input_script)
        format_csort(file_path=input_script, output_py=output_script, config_path=params.config_path)


if __name__ == "__main__":
    main()
