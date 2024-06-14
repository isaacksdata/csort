"""Module for logic to generate code difference strings"""
import ast
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import List

import libcst

from .utilities import get_expression_name


class DiffGenerator(ABC):
    """
    Abstract class for code difference generators.

    DiffGenerator classes are used for discerning the difference in the original python code and the msort formatted
    code. If msort is run with --diff flag then the differences are compiled into a human readable string to be
    printed on the terminal.

    Attributes:
        _source_code_methods (List[str]): names of methods of the class in original code
        _modified_code_methods (List[str]): names of methods of the class in msort formatted code
    """

    def __init__(self) -> None:
        self._source_code_methods: List[str] = []
        self._modified_code_methods: List[str] = []

    @abstractmethod
    def _extract_method_names(self, methods: List[Any]) -> List[str]:
        """
        Abstract method for extracting names from methods
        Args:
            methods: input list of methods of the class

        Returns:
            a list of identifiers extracted from methods
        """
        pass

    def diff(self, source_code: List[Any], msort_code: List[Any]) -> str:
        """
        Public method for finding difference between two lists of methods.

        Args:
            source_code: original list of methods in original order
            msort_code: msort formatted order of methods

        Returns:
            string representing the code changes between source_code and msort_code
        """
        self._source_code_methods = self._extract_method_names(source_code)
        self._modified_code_methods = self._extract_method_names(msort_code)
        return self._generate_diff_string()

    def _generate_diff_string(self) -> str:
        """
        Create a diff representation from method names.

        e.g.

        [0]   my_private_func ----> my_static_func
        [1]   my_static_func  ----> my_private_func

        This indicates that the first method was a private method but has been swapped with the static method.

        Returns:
            string representing code differences
        """
        if self._source_code_methods == self._modified_code_methods:
            return "No changes made!"
        lines = []
        longest_source_name = max(len(method) for method in self._source_code_methods)
        for i, (source_name, dest_name) in enumerate(zip(self._source_code_methods, self._modified_code_methods)):
            lines.append(
                f"[{i}] : {source_name}{' ' * (longest_source_name - len(source_name))}     --->     {dest_name}"
            )
        return "\n".join(lines)


class SyntaxTreeDiffGenerator(DiffGenerator):
    """
    Concrete class for generating code difference strings when the code has been parsed with AST or CST
    """

    def _extract_method_names(self, methods: List[Any]) -> List[str]:
        """
        Implements identifier extraction from AST/CST parsed code nodes
        Args:
            methods: input list of AST/CST parsed methods

        Returns:
            a list of identifiers extracted from methods

        Raises:
            TypeError: if any of the methods are not AST/CST parsed
        """
        methods = [list(m.keys())[0] if isinstance(m, dict) else m for m in methods]
        if not all(isinstance(method, (ast.AST, libcst.CSTNode)) for method in methods):
            raise TypeError("Unexpected code type!")
        return [get_expression_name(method) for method in methods]
