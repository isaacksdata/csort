from typing import List

import black


def add_func(x: int, y: int) -> int:
    return x + y


class MyClass:
    def __init__(self):
        self._name = "myclass"
        print(123)
        print(456)

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

    @classmethod
    def a_class_method(cls):
        pass

    @name.getter
    def name(self):
        return self._name


def subtract_func(x: int, y: int) -> int:
    return x - y


x1 = 5
y1 = 10

if __name__ == "__main__":
    print(add_func(x1, y1))
    print(subtract_func(x1, y1))
