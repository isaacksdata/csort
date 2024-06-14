"""Constants used throughout the project"""
import ast
from typing import Any
from typing import Dict
from typing import Final
from typing import List
from typing import Protocol
from typing import TypedDict
from typing import Union

import libcst

# pattern used to define magic dunder methods e.g. "__init__()"
DUNDER_PATTERN: Final[str] = "__"

# default sorting level to use for instance methods e.g. def func(self): ...
INSTANCE_METHOD_LEVEL: Final[int] = 12

# spacing between class definitions
CLASS_SPACING: Final[str] = "\n\n\n"

# Default name for a docstring expression
DOCSTRING_NAME: Final[str] = "docstring"

# Name of ini config file
DEFAULT_CONFIG_INI_FILE_NAME: Final[str] = "msort.ini"

# Name of toml config file
DEFAULT_CONFIG_TOML_FILE_NAME: Final[str] = "pyproject.toml"

# Name of subsection indicating method ordering
DEFAULT_MSORT_ORDERING_SUBSECTION: Final[str] = "order"

# Name of ordering subsection of msort.ini
DEFAULT_MSORT_ORDERING_SECTION: Final[str] = f"msort.{DEFAULT_MSORT_ORDERING_SUBSECTION}"

# Name of other msort params config section
DEFAULT_MSORT_PARAMS_SECTION: Final[str] = "msort"

# Default config file parameters
DEFAULT_MSORT_ORDER_PARAMS: Final[Dict[str, Any]] = {
    "dunder_method": 3,
    "msort_group": 4,
    "class_method": 5,
    "static_method": 6,
    "property": 7,
    "getter": 8,
    "setter": 9,
    "deleter": 10,
    "decorated_method": 11,
    "instance_method": INSTANCE_METHOD_LEVEL,
    "private_method": 13,
    "inner_class": 14,
}

DEFAULT_MSORT_GENERAL_PARAMS: Final[Dict[str, Any]] = {
    "use_msort_group": True,
    "auto_static": True,
    "use_property_groups": False,
}
find_classes_response = TypedDict("find_classes_response", {"node": Union[ast.ClassDef, libcst.CSTNode], "index": int})
format_msort_response = TypedDict("format_msort_response", {"code": int, "diff": str})
ordered_methods_type = List[Union[ast.stmt, Dict[ast.stmt, "ordered_methods_type"]]]
Node = Union[ast.stmt, libcst.CSTNode]

# Protocols


class Readable(Protocol):
    @staticmethod
    def read(config_path: str) -> Dict[str, Any]:  # pragma: no cover
        ...
