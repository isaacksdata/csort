class MyClass:
    def __init__(self):
        self._name = "myclass"
        self._age = 5

    @property
    def age(self):
        return self._age

    @age.getter
    def age(self):
        return self._age

    @age.setter
    def age(self, new_age: str):
        self._age = new_age

    @age.deleter
    def age(self):
        del self._age

    @property
    def name(self):
        return self._name

    @name.getter
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @name.deleter
    def name(self):
        del self._name
