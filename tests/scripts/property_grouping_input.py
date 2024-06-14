class MyClass:
    def __init__(self):
        self._name = "myclass"
        self._age = 5

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def age(self):
        return self._age

    @name.getter
    def name(self):
        return self._name

    @age.deleter
    def age(self):
        del self._age

    @name.deleter
    def name(self):
        del self._name

    @age.setter
    def age(self, new_age: str):
        self._age = new_age

    @age.getter
    def age(self):
        return self._age
