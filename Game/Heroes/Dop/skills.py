import random
from ...Interface.interface import InterfaceManager
from . import states, effects

interface = InterfaceManager.instance()


class SkillCard:
    name = ''
    energy = 0
    freq = 0
    description = ''

    needed_hero_states = []
    needed_enemy_states = []

    def check_effects_on_player(self, player):
        result = True
        for state in self.needed_hero_states:
            if state not in player.states_names():
                result = False
                interface.print_msg(f"У {self.name} нету состояния {state}.")
        return result

    def cast(self, player, enemy):
        raise NotImplementedError

    def after_cast(self, player, enemy):
        player.take_energy(self.energy + player.energy_penalty)
        self.player_remove_skill_from_arm(player)
        player.increase_penalty()

    def player_remove_skill_from_arm(self, player):
        player.remove_skill_from_arm(self)

    def __str__(self):
        text = f"-|{self.name}|- ({self.energy})"
        return text


class SimpleKick(SkillCard):
    name = 'Простой удар'
    energy = 3
    freq = 5
    description = f'Вы наносите выбранному врагу <strength> урона'

    def cast(self, player, enemy):
        number = interface.choose_one_from_list(enemy.alive_team, short_str=True)
        if number == 0:
            return False
        hero = enemy.alive_team[number - 1]
        interface.print_line()
        interface.print_msg(f"{player.name} наносит простой ударчик по {hero.name}...")
        hero.get_damage(player.strength)
        interface.print_line()
        self.after_cast(player, enemy)


class PlevokOtchaiania(SkillCard):
    name = 'Плевок отчаяния'
    energy = 2
    freq = 3
    value = 35

    description = f'Вы отчаянно соскребываете слюну с десен и плюете ею во врага.\n' \
                  f'Зачем? - спросите вы. Вы прибавите противнику #влажность + {value}'

    def cast(self, player, enemy):
        number = interface.choose_one_from_list(enemy.team, short_str=True)
        if number == 0:
            return False
        hero = enemy.team[number - 1]
        interface.print_msg(f"ХУЯК - плевчина смачно приземлилась на лицо {hero.name}...")
        effect = effects.Wetness(self.value)
        hero.get_effect(effect)
        self.after_cast(player, enemy)


class Podgotovlenie(SkillCard):
    name = 'подготовление'
    energy = 2
    freq = 2
    description = 'Вы тратите 2 энергии, и готовите в руку 2 карты умений'

    def cast(self, player, enemy):
        interface.print_msg("*звуки подготовки*")
        player.pick_up_cards()
        player.pick_up_cards()
        self.after_cast(player, enemy)


class UdarSRazvorota(SkillCard):
    name = 'удар рукой с разворота'
    energy = 4
    freq = 2
    description = "Если вы <развернуты>, вы можете нанести удар с разворота, хорошенько трепанув соперника.\n" \
                  "При этом вы нанесете ему <strength> * 2 урона, а так-же с 50% шансом повалите врага на пол.\n" \
                  "Иначе вы можете <развернуться> на 1 ход, не теряя энергию, и добрать карту."

    needed_hero_states = ['развернут']

    def cast(self, player, enemy):
        result = self.check_effects_on_player(player)
        if result:
            number = interface.choose_one_from_list(enemy.team, short_str=True)
            if number == 0:
                return False
            hero = enemy.team[number - 1]
            hero.get_damage(player.strength * 2)

            if interface.check_chance(50):
                enemy.get_effect(states.Fallen(1))
            else:
                print(f"{enemy.name} устоял на ногах")
            player.remove_effect_by_name('развернут')
            self.after_cast(player, enemy)
        else:
            ans = input(f"Вы не можете ударить. Хотите использовать второй вариант? (y/n): ")
            if ans == 'y':
                player.get_effect(states.TurnedAround(1))
                player.pick_up_cards()
                self.player_remove_skill_from_arm(player)
            else:
                return False


class PnutLezhachih(SkillCard):
    name = 'пнуть лежачих'
    energy = 2
    freq = 2
    description = 'Вы пинаете <упавшего> врага и наносите ему <strength>/2 + <fighting> урона.\n' \
                  'С шансом 25 % вы продливаете его лежачесть на 1.'

    def cast(self, player, enemy):
        print(f"Выберите лежачего врага")
        laying_enemies = list(filter(lambda enemy: 'упавший' in enemy.states_names(), enemy.team))
        number = interface.choose_one_from_list(laying_enemies, short_str=True)
        if number == 0:
            return False
        hero = laying_enemies[number - 1]

        hero.get_damage(round(player.strength / 2) + player.fighting)
        if interface.check_chance(25):
            print(f"Также удалось прибить врага к земле")
            hero.get_state(states.Fallen(1))
        self.after_cast(player, enemy)



classes = [
    SimpleKick,
    PlevokOtchaiania,
    Podgotovlenie,
    UdarSRazvorota,
    PnutLezhachih
]
