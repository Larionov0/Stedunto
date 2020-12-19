from . import states
from Game.Interface import colors


class Effect:
    name = 'state'
    value = 0
    max_value = 100
    color = None

    def __init__(self, value):
        self.value = value

    def increase_value(self, value, hero):
        self.value += value
        self.check_on_max(hero)

    def check_on_max(self, hero):
        if self.value > self.max_value:
            self.value = self.max_value
            self.on_max_reaching(hero)
            hero.remove_effect(self)

    def decrease_value(self, value, hero):
        self.value -= value
        if self.value <= 0:
            hero.remove_state(self)

    def on_max_reaching(self, hero):
        pass

    def __str__(self):
        return f"#{self.name}: {self.value}/{self.max_value}"


class Wetness(Effect):
    name = 'влажность'
    max_value = 100
    color = colors.CBLUE2

    def on_max_reaching(self, hero):
        hero.get_effect(
            states.Soaking(2)
        )


class Laughing(Effect):
    name = 'смех'
    max_value = 100

    def on_max_reaching(self, hero):
        print(f"{hero.name} захохотался(ась) так, что была оглушена")
        hero.get_effect(
            states.Stun(1)
        )
