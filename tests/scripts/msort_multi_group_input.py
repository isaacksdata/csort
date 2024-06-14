from msort import msort_group


class Dog:
    def __init__(self, name: str, color: str, owner: str) -> None:
        self.name = name
        self.color = color
        self.owner = owner

    @msort_group(group="sound")
    def bark(self) -> None:
        print("The dog is barking!")

    @msort_group(group="describe")
    def color_of_dog(self) -> None:
        print(f"The dog is {self.color}")

    @msort_group(group="describe")
    def describe(self) -> None:
        print(f"The dog called {self.name} is owned by {self.owner}")

    @msort_group(group="sound")
    def growling(self) -> None:
        print("The dog is growling!")

    @msort_group(group="movement")
    def run(self) -> None:
        print("The dog is running!")

    @msort_group(group="movement")
    def wag(self) -> None:
        print("The dog is wagging its tail!")

    @msort_group(group="movement")
    def walk(self) -> None:
        print("The dog is walking!")

    @msort_group(group="sound")
    def whimper(self) -> None:
        print("The dog is whimpering!")
