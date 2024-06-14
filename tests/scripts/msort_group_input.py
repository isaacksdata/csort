from abc import abstractmethod
from functools import lru_cache
from functools import wraps

from src import msort_group


class MyClass:
    def __init__(self):
        self._name = "myclass"

    @abstractmethod
    def func(self):
        pass

    @msort_group("test")
    def _func(self):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    def __len__(self):
        pass

    @msort_group("test")
    @staticmethod
    def a_static_method():
        pass

    @lru_cache
    @staticmethod
    def a_static_cached_method():
        pass

    @wraps
    def wrapped_func(self):
        pass

    @lru_cache
    def second_cached_func(self):
        pass

    @wraps
    @abstractmethod
    def wrapped_abstract_func(self):
        pass

    @classmethod
    def a_class_method(cls):
        pass

    @name.getter
    @wraps
    @lru_cache
    def name(self):
        return self._name

    @lru_cache
    def cached_func(self):
        pass
