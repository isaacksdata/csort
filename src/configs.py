"""Constants used throughout the project"""
from typing import Any
from typing import Dict
from typing import Final

# pattern used to define magic dunder methods e.g. "__init__()"
DUNDER_PATTERN: Final[str] = "__"

# default sorting level to use for instance methods e.g. def func(self): ...
INSTANCE_METHOD_LEVEL: Final[int] = 11

# spacing between class definitions
CLASS_SPACING: Final[str] = "\n\n\n"

# Default name for a docstring expression
DOCSTRING_NAME: Final[str] = "docstring"

# Name of ini config file
DEFAULT_CONFIG_FILE_NAME: Final[str] = "csort.ini"

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

DEFAULT_CSORT_GENERAL_PARAMS: Final[Dict[str, Any]] = {
    "use_csort_group": True,
}
