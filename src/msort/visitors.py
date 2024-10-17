"""A module for defining visitors"""
from typing import List
from typing import Optional
from typing import Tuple

import libcst
import libcst as cst


class MethodCallVisitor(cst.CSTVisitor):
    """
    A visitor which records the dependencies between class methods
    """

    def __init__(self) -> None:
        super().__init__()
        self.calls: List[Tuple[str, str]] = []
        self.current_method: Optional[str] = None

    def get_function_name(self, node: cst.CSTNode) -> Optional[str]:
        """
        Get the name of a CST function
        Args:
            node: current CST node

        Returns:
            name if found, else None
        """
        if isinstance(node, cst.Name):
            return node.value
        elif isinstance(node, cst.Attribute):
            return node.attr.value
        return None

    def leave_FunctionDef(self, node: cst.FunctionDef) -> None:
        """
        Complete the visit by setting current_method back to None
        Args:
            node: current node

        Returns:
            void
        """
        self.current_method = None

    def visit_Call(self, node: cst.Call) -> None:
        """
        Check for a relationship between functions and record it if it exists in self.calls
        Args:
            node: current Call node

        Returns:
            void
        """
        if self.current_method:
            function_name = self.get_function_name(node.func)
            if function_name and self._is_attribute(node.func):
                self.calls.append((self.current_method, function_name))

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        """
        Visit the current node by setting the node to the current_method attribute
        Args:
            node: the current node

        Returns:
            void
        """
        self.current_method = node.name.value

    def _is_attribute(self, node: cst.CSTNode) -> bool:
        return isinstance(node, libcst.Attribute)
