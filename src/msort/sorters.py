"""
Module containing Sorter classes which implement logic for sorting methods using different rules
"""
import logging
from abc import ABC
from abc import abstractmethod
from collections import defaultdict
from types import ModuleType
from typing import Dict
from typing import List
from typing import Optional

from .configs import Node
from .configs import ordered_methods_type
from .decorators import has_decorator
from .method_describers import describe_method
from .method_describers import MethodDescriber
from .utilities import get_function_name
from .visitors import MethodCallVisitor


class Sorter(ABC):
    """
    Base Sorter class
    """

    def __init__(self, parser: ModuleType) -> None:
        self.parser = parser

    @abstractmethod
    def sort(self, methods: List[Node], parent: Optional[Node] = None) -> ordered_methods_type:
        pass

    def _recursive_sort(self, methods: List[Node]) -> ordered_methods_type:
        formatted_sorted_methods: ordered_methods_type = [
            {m: self.sort(methods=self.parser.extract_class_components(m), parent=m)}
            if self.parser.is_class(m) or self.parser.contains_class(m)
            else m
            for m in methods
        ]
        return formatted_sorted_methods


class DescriptionSorter(Sorter):
    def __init__(self, parser: ModuleType, method_describer: MethodDescriber) -> None:
        super().__init__(parser)
        self.method_describer = method_describer

    def sort(self, methods: List[Node], parent: Optional[Node] = None) -> ordered_methods_type:
        sorted_methods = self._initial_sort(methods, parent)
        formatted_sorted_methods = self._recursive_sort(sorted_methods)
        return formatted_sorted_methods

    def _initial_sort(self, methods: List[Node], parent: Optional[Node] = None) -> List[Node]:
        if parent is None or self.parser.is_class(parent):
            sorted_methods: List[Node] = sorted(methods, key=lambda m: describe_method(m, self.method_describer))
        else:
            sorted_methods = methods
        return sorted_methods


class PropertyGroupSorter(DescriptionSorter):
    def sort(self, methods: List[Node], parent: Optional[Node] = None) -> ordered_methods_type:
        sorted_methods = self._initial_sort(methods, parent)
        sorted_methods = self._property_sort(sorted_methods)
        formatted_sorted_methods = self._recursive_sort(sorted_methods)
        return formatted_sorted_methods

    def _property_sort(self, methods: List[Node]) -> List[Node]:
        # find index of properties
        prop_idx = [i for i, method in enumerate(methods) if has_decorator(method, "property")]
        original_order = methods.copy()
        # iterate over properties and find methods with the same name
        for prop in prop_idx:
            updated_prop = methods.index(original_order[prop])
            attr_name = get_function_name(methods[updated_prop])
            # sort by property, getter, setter, deleter
            funcs = sorted(
                [method for method in methods if get_function_name(method) == attr_name],
                key=lambda m: describe_method(m, self.method_describer),
            )
            methods = [m for m in methods if m not in funcs]
            methods = methods[:updated_prop] + funcs + methods[updated_prop:]
        return methods


class CallStackSorter(Sorter):
    def __init__(self, parser: ModuleType):
        super().__init__(parser)
        self.visitor = MethodCallVisitor()

    def sort(self, methods: List[Node], parent: Optional[Node] = None) -> ordered_methods_type:
        # visit each method
        for method in methods:
            method.visit(self.visitor)

        # instantiate method name: method dictionary
        methods_mapping: Dict[str, Node] = {m.name.value: m for m in methods}

        # create adjacency list
        adjacency_list = defaultdict(list)
        for caller, callee in self.visitor.calls:
            adjacency_list[caller].append(callee)

        # topological sort
        sorted_method_names = self._dfs(graph=adjacency_list)
        sorted_methods = [methods_mapping[m] for m in sorted_method_names]

        # add back in dunder methods
        dunder_method_names = sorted(
            [name for name, method in methods_mapping.items() if self.parser.is_dunder_method(method)]
        )
        dunder_methods = [methods_mapping[name] for name in dunder_method_names]
        sorted_methods = [*dunder_methods, *sorted_methods]

        # add back in any missing methods from method mapping
        isolated_method_names = sorted(
            [name for name, method in methods_mapping.items() if method not in sorted_methods]
        )
        isolated_methods = [methods_mapping[name] for name in isolated_method_names]
        sorted_methods = [*sorted_methods, *isolated_methods]

        # recursive sort
        formatted_sorted_methods = self._recursive_sort(methods=sorted_methods)

        return formatted_sorted_methods

    def _dfs(self, graph: Dict[str, List[str]]) -> List[str]:
        reversed_graph = self._reverse_graph(graph)
        visited = set()
        stack = []

        def __inner_dfs(node: str) -> None:
            if node not in visited:
                visited.add(node)
                for neighbor in list(reversed_graph.get(node, [])):
                    __inner_dfs(neighbor)
                stack.append(node)

        for node in list(reversed_graph.keys()):
            __inner_dfs(node)

        return stack

    def _reverse_graph(self, graph: Dict[str, List[str]]) -> Dict[str, List[str]]:
        reversed_graph = defaultdict(list)
        for node in graph:
            for neighbor in graph[node]:
                reversed_graph[neighbor].append(node)
        return reversed_graph


def get_sorter(
    parser: ModuleType,
    method_describer: MethodDescriber,
    use_property_groups: bool = False,
    use_directed_graph: bool = False,
) -> Sorter:
    if use_property_groups and use_directed_graph:
        logging.warning("Cannot use property groups and directed graph! Directed graph taking precedent!")
        use_property_groups = False
    if use_directed_graph:
        sorter = CallStackSorter(parser=parser)
    elif use_property_groups:
        sorter = PropertyGroupSorter(parser=parser, method_describer=method_describer)
    else:
        sorter = DescriptionSorter(parser=parser, method_describer=method_describer)
    return sorter
