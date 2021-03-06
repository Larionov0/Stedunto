from ..Heroes.hero import Hero
from ..Interface.interface import InterfaceManager

interface = InterfaceManager.instance()


class HeroBattle:
    @staticmethod
    def heroes_starts_battle(hero1: Hero, hero2: Hero):
        for hero in hero1.alive_team:
            hero.before_battle(hero2)
        for hero in hero2.alive_team:
            hero.before_battle(hero1)

        while True:
            for hero in hero1.alive_team:
                if len(hero2.alive_team) != 0:
                    hero.make_move()
            for hero in hero2.alive_team:
                if len(hero1.alive_team) != 0:
                    hero.make_move()

            if len(hero1.alive_team + hero2.alive_team) == 0:
                return 0
            elif not hero1.is_team_alive:
                interface.print_msg(f"{hero2.colored_name} победил!")
                return hero2
            elif not hero2.is_team_alive:
                interface.print_msg(f"{hero1.colored_name} победил!")
                return hero1
