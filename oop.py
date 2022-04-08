from dataclasses import dataclass
from typing import Optional


class Creature:
    conscious: bool
    humanoid: bool

    def conscious_act(self):
        if self.conscious:
            print("conscious")
        else:
            print("unconscious")


class Human(Creature):
    first_name: str
    last_name: Optional[str]
    age: int
    parent1_id: int
    parent2_id: Optional[int]
    gender: str
    country: str

    def speech(self, words):
        print(f"{self.first_name} says '{words}'")

    def __init__(self, id, first_name, last_name, age, parent1_id, gender, country, parent2_id=None):
        self.conscious = True
        self.humanoid = True
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.parent1_id = parent1_id
        self.gender = gender
        self.country = country
        self.parent2_id = parent2_id
        


class Dogs(Creature):
    conscious = True
    humanoid = False
    name: str
    age: int
    gender: str

    def bark(self, sound):
        print(f"{self.name} barks '{sound}'")


@dataclass
class Bacteria(Creature):
    conscious = False
    humanoid = False
    name: str

    def dn(self, amount):
        print(f"{self.name} do nothing for {amount} secs")


clarissa = Human


if __name__ == '__main__':
    pass
