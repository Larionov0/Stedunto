from Game.Heroes.hero import Hero, Mob, Boss, states
import random
from Game.Interface.interface import InterfaceManager

interface = InterfaceManager.instance()


class Prespeshnik(Mob):
    name = 'Prespeshnik'
    hp = max_hp = 300
    armor = 3

    def __init__(self, team=None):
        super().__init__(team)
        self.hp = random.randint(80, 150)

    def what_to_do(self):
        print(f'{self.colored_name}: "Уйдите немедленно!"')
        for _ in range(3):
            random.choice(self.enemy.alive_team).get_damage(20)


class Chert(Boss):
    name = 'Chert'
    hp = max_hp = 10000
    armor = 5

    def before_battle(self, enemy):
        super().before_battle(enemy)
        for _ in range(3):
            p = Prespeshnik(self.team)
            p.enemy = self.enemy
            self.team.add_hero(p)

    def what_to_do(self):
        interface.print_msg("ЧЕРТ СОБИРАЕТСЯ ТРАХНУТЬ ВАС!")
        choice = random.randint(1, 5)

        if choice in (1, 2):
            text = 'ДЕДЛАЙНОВЫЙ КРЮК\n' \
                   'Черт вытягивает дедлайновым крюком троих противников и наносит тем по 200 урона'
            interface.print_msg(text)

            for _ in range(3):
                if self.enemy.is_team_alive:
                    hero = random.choice(self.enemy.alive_team)
                    hero.get_damage(200)

        elif choice in (3, 4):
            text = "Массовая истерия\n" \
                   "Черт вызывает массовую истерию у каждого второго противника, накладывая на того\n" \
                   "кровотечение из носа на 10 ходов и нанося 66 урона душевной боли"
            interface.print_msg(text)
            for hero in self.enemy.alive_team:
                if interface.check_chance(50):
                    hero.get_state(states.Bleeding(10))
                    hero.get_damage(66)

        elif choice == 5:
            text = f"Адский смех\n" \
                   f"Черт издает адский смех, оглушая каждого на 1-2 хода"
            interface.print_msg(text)
            for hero in self.enemy.alive_team:
                hero.get_state(states.Stun(random.randint(1, 2)))
