"""
Decorator which can be added to class functions to control ordering by group name
"""
import inspect
import logging
from typing import Any
from typing import Callable


def csort_group(group: str) -> Callable:
    """
    Decorator to enable sorting of functions by user defined functional groups.
    Args:
        group: name to give to the functional group

    Returns:
        decorator function

    Examples:

        class MyClass:

            @csort_group(group="addition")
            def func():
                return 1 + 1

            @csort_group(group="addition")
            def related_func():
                return 2 + 2
    """

    def decorator(func: Callable) -> Callable:
        # This function will be called when the decorator is applied
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Call the original function
            result = func(*args, **kwargs)
            logging.debug("Calling %s with csort_group : group = %s", func.__qualname__, group)
            return result

        if not inspect.isfunction(func) and not inspect.ismethod(func):
            raise TypeError(f"csort_group should be applied to a function - not {type(func)}")

        # this check does not handle nested functions outside of classes - but in this case, csort will not do
        # anything
        if "." not in func.__qualname__:
            logging.warning(
                "csort_group decorator applied to a function which is not implemented by a class : %s",
                func.__qualname__,
            )

        return wrapper

    return decorator
