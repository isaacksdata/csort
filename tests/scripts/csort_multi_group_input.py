from csort import csort_group


class Dog:
    def __init__(self, name: str, color: str, owner: str) -> None:
        self.name = name
        self.color = color
        self.owner = owner

    @csort_group(group="sound")
    def bark(self) -> None:
        print("The dog is barking!")

    @csort_group(group="describe")
    def color_of_dog(self) -> None:
        print(f"The dog is {self.color}")

    @csort_group(group="describe")
    def describe(self) -> None:
        print(f"The dog called {self.name} is owned by {self.owner}")

    @csort_group(group="sound")
    def growling(self) -> None:
        print("The dog is growling!")

    @csort_group(group="movement")
    def run(self) -> None:
        print("The dog is running!")

    @csort_group(group="movement")
    def wag(self) -> None:
        print("The dog is wagging its tail!")

    @csort_group(group="movement")
    def walk(self) -> None:
        print("The dog is walking!")

    @csort_group(group="sound")
    def whimper(self) -> None:
        print("The dog is whimpering!")
