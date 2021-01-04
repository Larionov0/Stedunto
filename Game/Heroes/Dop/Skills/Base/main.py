from ..skill import SkillCard, interface
from Game.globals import STRENGTH, ENERGY
from Game.Heroes.Dop import states


class PryamayaTychka(SkillCard):
    name = 'Прямая тычка'
    energy = 3
    freq = 6
    description = f'Вы совершаете стандартную атаку по выбранному противнику,\n' \
                  f'нанося {STRENGTH} урона и ничего особенного не происходит.'

    def cast(self, player, enemy):
        hero = interface.choose_one_from_list(enemy.alive_team, short_str=True)
        if hero == 0:
            return False
        interface.print_line()
        interface.print_msg(f"{player.name} наносит простой ударчик по {hero.name}...")
        hero.get_damage(player.strength)
        interface.print_line()
        self.after_cast(player, enemy)


class UdarSRazmahu(SkillCard):
    name = 'Удар с размаху'
    energy = 3
    freq = 3
    description = f'Герой совершает атаку по выбранному врагу, нанося тому {STRENGTH} + 4 урона.'
    needed_hero_states = ['готовность']

    def cast(self, player, enemy):
        hero = interface.choose_one_from_list(enemy.alive_team, short_str=True)
        if hero == 0:
            return False
        interface.print_line()
        interface.print_msg(f"{player.name} наносит удар с размаху по {hero.name}...")
        hero.get_damage(player.strength + 4)
        interface.print_line()
        self.after_cast(player, enemy)


class SmenaStoiki(SkillCard):
    name = 'Смена стойки'
    energy = 0
    freq = 2
    is_soft = True
    description = f'Герой восстанавливает 2 {ENERGY} и получает состояние [Готовность] на ход '
    needed_hero_states = []

    def cast(self, player, enemy):
        player.add_energy(2)
        player.get_state(
            states.Ready(1)
        )
        self.after_cast(player, enemy)


skills = [PryamayaTychka, UdarSRazmahu, SmenaStoiki]
