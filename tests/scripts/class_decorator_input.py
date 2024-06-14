from dataclasses import dataclass


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

    @dataclass
    class NestedDataClass:
        name: str


@dataclass
class Book:
    title: str
    author: str
    publication_year: int
    pages: int
    genre: str

    def is_classic(self) -> bool:
        # Consider a book classic if it's more than 50 years old
        return (2024 - self.publication_year) > 50

    def __post_init__(self) -> None:
        # Example of a post-initialization process
        self.description = f"{self.title} by {self.author}, published in {self.publication_year}."
