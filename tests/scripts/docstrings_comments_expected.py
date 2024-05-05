"""This is a module level docstring"""


class MyClass:
    """
    This is my class docstring

    It is a test class to test that Csort preserves docstrings and comments

    Attributes:
        _name: some name

    Methods:
        func
        _func
    """

    def __init__(self):
        """
        Init the class
        """
        self._name = "myclass"
        print(123)
        print(456)  # inline comment

    def __len__(self):
        # comment
        pass  # followed by inline comment

    @classmethod
    def a_class_method(cls):
        pass

    @staticmethod
    def a_static_method():
        pass

    @property
    def name(self):
        # access the self._name attribute
        return self._name

    @name.getter
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """
        Set the name attribute
        Args:
            new_name: new name

        Returns:
            void
        """
        # adding a double line comment
        # here is the second line
        self._name = new_name

    def commented_func(self):  # todo add annotation
        # this ia function with some comments
        x = 1  # comment about x
        # now returning x
        return x

    def func(self):
        pass

    def _func(self):
        """
        This is a private function
        Returns:
            void
        """
        pass
