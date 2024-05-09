"""
Command line entrypoint for Csort
"""
import argparse

from src.formatting import format_csort


def parse_commandline() -> argparse.Namespace:
    """Parse CLI arguments using argparse"""
    parser = argparse.ArgumentParser(
        description="Takes as input the path to .py file or directory containing .py files and re-orders methods of "
        "classes according to Csort guidelines."
    )
    parser.add_argument(
        "--input-path",
        type=str,
        default="./",
        help="Relative filepath to python source code files",
    )
    parser.add_argument(
        "--output-path",
        type=str,
        default=None,
        help="Relative filepath to where formatted source should be saved. If None, then original files will be "
        "modified.",
    )
    parser.add_argument(
        "--config-path",
        type=str,
        default=None,
        help="Relative filepath to a csort.ini file.",
    )
    params = parser.parse_args()

    return params


def main() -> None:
    params = parse_commandline()

    # todo something here to handle single files vs directories

    format_csort(file_path=params.input_path, output_py=params.output_path, config_path=params.config_path)


if __name__ == "__main__":
    main()
