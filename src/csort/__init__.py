from importlib.metadata import version

from .csort_decorator import csort_group
from .formatting import format_csort

dist_name = "csort"
__version__ = version(dist_name)
