"""Constants used throughout the project"""
import ast
from typing import Any
from typing import Dict
from typing import Final
from typing import Protocol
from typing import TypedDict
from typing import Union

import libcst

# pattern used to define magic dunder methods e.g. "__init__()"
DUNDER_PATTERN: Final[str] = "__"

# default sorting level to use for instance methods e.g. def func(self): ...
INSTANCE_METHOD_LEVEL: Final[int] = 11

# spacing between class definitions
CLASS_SPACING: Final[str] = "\n\n\n"

# Default name for a docstring expression
DOCSTRING_NAME: Final[str] = "docstring"

# Name of ini config file
DEFAULT_CONFIG_INI_FILE_NAME: Final[str] = "csort.ini"

# Name of toml config file
DEFAULT_CONFIG_TOML_FILE_NAME: Final[str] = "pyproject.toml"

# Name of subsection indicating method ordering
DEFAULT_CSORT_ORDERING_SUBSECTION: Final[str] = "order"

# Name of ordering subsection of csort.ini
DEFAULT_CSORT_ORDERING_SECTION: Final[str] = f"csort.{DEFAULT_CSORT_ORDERING_SUBSECTION}"

# Name of other csort params config section
DEFAULT_CSORT_PARAMS_SECTION: Final[str] = "csort"

# Default config file parameters
DEFAULT_CSORT_ORDER_PARAMS: Final[Dict[str, Any]] = {
    "dunder_method": 3,
    "csort_group": 4,
    "class_method": 5,
    "static_method": 6,
    "property": 7,
    "getter": 8,
    "setter": 9,
    "decorated_method": 10,
    "instance_method": 11,
    "private_method": 12,
}

DEFAULT_CSORT_GENERAL_PARAMS: Final[Dict[str, Any]] = {"use_csort_group": True, "auto_static": True}
find_classes_response = TypedDict("find_classes_response", {"node": Union[ast.ClassDef, libcst.CSTNode], "index": int})
format_csort_response = TypedDict("format_csort_response", {"code": int, "diff": str})

# Protocols


class Readable(Protocol):
    @staticmethod
    def read(config_path: str) -> Dict[str, Any]:
        ...
