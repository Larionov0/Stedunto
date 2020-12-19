from Game.Heroes.hero import Hero, Mob
import random
from Game.Interface.interface import InterfaceManager

interface = InterfaceManager.instance()


class Pervash(Mob):
    all_phrases = [
        'Ты у меня получишь!',
        'Надоело!!!',
        "Получайте, скоты",
        "Это революция!!",
        "Ненавижу тварей",
        "Лучше уж так, чем оставить как есть",
        "Перебью нахрен",
        "Это тебе за тех двоих",
        "Получай, ублюдок",
        "Теперь то вышли на встречу, скотины",
        "Сейчас вы у нас попляшете",
        "Нехуй было устраивать этот гнет!",
        "Ах вы уроды"
    ]
    all_names = ['Толик', "Каря", "Маша", "Даша", "Василий", "Рома", "Женя", "Евгений", "Боря", "Антон", "Василиса", "Настя", "Ира", "Саша", "Алекс", "Боб", "Биба", "Боба"]

    def __init__(self, team=None):
        super().__init__(team)
        self.name = 'Перваш ' + random.choice(self.all_names)
        self.hp = self.max_hp = random.randint(90, 210)
        self.strength = 10

    def what_to_do(self):
        print(f"\n{self.colored_name}: '{random.choice(self.all_phrases)}'\n")
        hero = random.choice(self.enemy.alive_team)
        hero.get_damage(self.strength)
