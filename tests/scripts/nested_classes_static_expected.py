class MyClass:
    def __init__(self):
        self._name = "myclass"
        print(123)
        print(456)

    def __len__(self):
        pass

    @classmethod
    def a_class_method(cls):
        pass

    @staticmethod
    def _func():
        pass

    @staticmethod
    def a_static_method():
        pass

    @staticmethod
    def func():
        pass

    @property
    def name(self):
        return self._name

    @name.getter
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    class AnotherNestedClass:
        def __init__(self):
            self.name = "another-nested-class"

        def func(self):
            print(self.name)

    class NestedClass:
        def __init__(self):
            self.name = "nested-class"

        @staticmethod
        def func():
            print("nested-class")

        class InnerNestedClass:
            def __init__(self):
                self.name = "inner-nested-class"

            @staticmethod
            def func():
                print("inner-nested-class")
