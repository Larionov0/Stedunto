from Game.Heroes.hero import Hero, Mob
import random
from Game.Interface.interface import InterfaceManager

interface = InterfaceManager.instance()


class Goblin(Mob):
    all_names = ['Швыньдяй', "Куки", "Барборо", "Глист", "Студень", "Сырник"]

    def __init__(self, team=None):
        super().__init__(team)
        self.name = 'Гоблин ' + random.choice(self.all_names)
        self.hp = self.max_hp = random.randint(40, 60)
        self.strength = 4

    def what_to_do(self):
        print(f"\n{self.colored_name}: 'Палучяй'\n")
        hero = random.choice(self.enemy.alive_team)
        hero.get_damage(self.strength)
