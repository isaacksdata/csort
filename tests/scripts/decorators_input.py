from abc import abstractmethod
from functools import lru_cache
from functools import wraps


class MyClass:
    def __init__(self):
        self._name = "myclass"

    @abstractmethod
    def func(self):
        pass

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

    @staticmethod
    def a_static_method():
        pass

    @wraps
    def wrapped_func(self):
        pass

    @lru_cache
    def second_cached_func(self):
        pass

    @classmethod
    def a_class_method(cls):
        pass

    @name.getter
    def name(self):
        return self._name

    @lru_cache
    def cached_func(self):
        pass
