class Creature:
    conscious: bool
    humanoid: bool

    def conscious_act(self):
        if self.conscious:
            print("conscious")
        else:
            print("unconscious")


class Human(Creature):
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

    def speech(self, words):
        print(f"{self.first_name} says '{words}'")
        

class Dogs(Creature):
    def __init__(self, name, age, breed=None):
        self.conscious = True
        self.humanoid = False
        self.name = name
        self.age = age
        self.breed = breed

    def bark(self, sound):
        print(f"{self.name} barks '{sound}'")


class Bacteria(Creature):
    def __init__(self, name, age):
        self.conscious = False
        self.humanoid = False
        self.name = name
        self.age = age

    def dn(self, at):
        print(f"{self.name} do nothing for {at} secs")


if __name__ == '__main__':
    pass
