from abc import abstractmethod
from functools import lru_cache
from functools import wraps


class MyClass:
    def __init__(self):
        self._name = "myclass"

    def __len__(self):
        pass

    @classmethod
    def a_class_method(cls):
        pass

    @staticmethod
    def a_static_method():
        pass

    @lru_cache
    @staticmethod
    def a_static_cached_method():
        pass

    @property
    def name(self):
        return self._name

    @name.getter
    @wraps
    @lru_cache
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @abstractmethod
    def func(self):
        pass

    @wraps
    @abstractmethod
    def wrapped_abstract_func(self):
        pass

    @lru_cache
    def cached_func(self):
        pass

    @lru_cache
    def second_cached_func(self):
        pass

    @wraps
    def wrapped_func(self):
        pass

    def _func(self):
        pass
