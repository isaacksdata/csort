from abc import abstractmethod


class MyClass:
    def __init__(self):
        self._name = "myclass"
        print(123)
        print(456)

    def __len__(self):
        return len(self._name)

    @classmethod
    def a_class_method(cls):
        pass

    @staticmethod
    def a_static_method() -> None:
        print("this is a static method")

    @staticmethod
    def a_static_method_already() -> None:
        print("this is a static method")

    @property
    def name(self):
        return self._name

    @name.getter
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @abstractmethod
    def abstract_method(self):
        pass

    def func(self):
        print(self.name)

    def not_a_static_method(self) -> None:
        print(f"{self._name}")

    def not_a_static_method_multi_lines(
        self,
        param1,
        param2,
    ) -> None:
        print(f"{self._name}")

    def _func(self):
        return self
