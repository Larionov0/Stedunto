from ..skill import SkillCard, interface
from Game.globals import STRENGTH, ENERGY, MAGIC
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


class PlusMinusRazryad(SkillCard):
    name = 'Плюс-минус-разряд'
    energy = 4
    freq = 2
    description = f'Если ты в состоянии [Готовность], выбери противника и проведи комбинацию, \n' \
                  f'завершающуюся смачным хлопком по ушам, это оглушит его на \n' \
                  f'ход и нанесет ему {STRENGTH} / 2 урона.\n' \
                  'Если нету состояния [Готовность], ты можешь потратить 4 hp на сие действо.'

    def cast(self, player, enemy):
        loose_hp = 0
        if 'готовность' not in player.states_names():
            print('У тебя нет состояния [Готовность]')
            ans = interface.press('Тратим 4 HP? (y/n)')
            if ans == 'y':
                loose_hp = 4
            else:
                return

        hero = interface.choose_one_from_list(enemy.alive_team, short_str=True)
        if hero is None:
            return

        player.loose_hp(loose_hp)

        hero.get_damage(interface.round(player.strength / 2))
        hero.get_state(states.Stun(1))
        self.after_cast(player, enemy)


class Izzhoga(SkillCard):
    name = 'Изжога'
    energy = 2
    freq = 200
    description = f'Ты бросаешь выбранному противнику курочку, он жадно на нее набрасывается,\n' \
                  f'но курочка оказывается переперченной, от чего у сьевшего начинается изжога.\n' \
                  f'[горение]: 5 + {MAGIC}'

    def cast(self, player, enemy):
        print('Выбери героя для подброса курочки:')
        hero = interface.choose_one_from_list(enemy.alive_team, short_str=True)
        if hero is None:
            return

        hero.get_state(states.Burning(5 + hero.magic))
        self.after_cast(player, enemy)


skills = [PryamayaTychka, UdarSRazmahu, SmenaStoiki, PlusMinusRazryad, Izzhoga]
