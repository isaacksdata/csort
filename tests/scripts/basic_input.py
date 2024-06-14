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

    @name.deleter
    def name(self):
        self.name = None

    @name.getter
    def name(self):
        return self._name
