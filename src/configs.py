"""Constants used throughout the project"""
from typing import Final

# pattern used to define magic dunder methods e.g. "__init__()"
DUNDER_PATTERN: Final[str] = "__"

# default sorting level to use for instance methods e.g. def func(self): ...
INSTANCE_METHOD_LEVEL: Final[int] = 9

# spacing between class definitions
CLASS_SPACING: Final[str] = "\n\n\n"
