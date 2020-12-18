from ..Heroes.hero import Hero


class HeroBattle:
    @staticmethod
    def heroes_starts_battle(hero1: Hero, hero2: Hero):
        hero1.before_battle(hero2)
        hero2.before_battle(hero1)

        while True:
            for hero in hero1.team:
                hero.make_move()
            for hero in hero2.team:
                hero.make_move()

            if all([not hero.alive for hero in hero1.team + hero2.team]):
                return 0
            elif all([not hero.alive for hero in hero1.team]):
                return hero1
            elif all([not hero.alive for hero in hero2.team]):
                return hero2
