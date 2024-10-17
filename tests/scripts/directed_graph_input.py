class MyClass:
    def __init__(self):
        self._name = "myclass"

    def _func(self):
        pass

    def _func2(self):
        pass

    def _func3(self):
        self._func2()

    def root(self):
        self._func()
        self._func3()
