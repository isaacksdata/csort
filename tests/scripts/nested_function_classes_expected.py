class MyClass:
    def __init__(self):
        self._name = "myclass"
        print(123)
        print(456)

    @staticmethod
    def a_static_method():
        pass

    @property
    def name(self):
        return self._name

    def func(self):
        pass

    def _func(self):
        class NestedClass:
            def __init__(self):
                self.name = "nested-class"

            def func(self):
                class InnerNestedClass:
                    def __init__(self, name: str):
                        self.name = name

                    def func(self):
                        print(self.name)

                inner_nested_class = InnerNestedClass(self.name)
                inner_nested_class.func()

        func_class = NestedClass()
        func_class.func()
