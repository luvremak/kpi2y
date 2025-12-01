class Character:
    def perform_action(self):
        raise NotImplementedError("Subclasses must implement this method.")


class Omori(Character):
    def perform_action(self):
        return "Omori read a sad poem. Omori feels sad."


class Aubrey(Character):
    def perform_action(self):
        return "Aubrey shouts 'You can do it'!"


class Kel(Character):
    def perform_action(self):
        return "Kel throws a ball wildly!"


class Hero(Character):
    def perform_action(self):
        return "Hero made snacks for everyone. Everybody feels better!"


class Something(Character):
    def perform_action(self):
        return "Something stares at you."

party = [
    Omori(),
    Aubrey(),
    Kel(),
    Hero(),
    Something()
]

for member in party:
    print(member.perform_action())
