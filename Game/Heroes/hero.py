from typing import List
from .Dop import effects, states
from ..Interface.interface import InterfaceManager
from ..Interface import colors
from ..Locations.place import Place


interface = InterfaceManager.instance()
ENERGY = f'{colors.CYELLOW}енергия{colors.CEND}'


class Hero:
    name = 'Hero'

    strength = 0
    mind = 0
    hp = max_hp = 0
    armor = 0
    magic = 0
    energy = max_energy = 10

    rage = 0
    max_rage = 100

    _standard_team_number = 2
    place: Place = None

    sex = 'М'
    enemy = None

    alive = True
    is_user_control = True

    can_use_skill = True
    can_make_move = True

    def __init__(self, team=None, place=None):
        self.enemy: Hero = self.enemy

        if team is None:
            team = Team(self._standard_team_number, [self])
        self.team = team
        self.place = place
        self.effects: List[effects.Effect] = []
        self.states: List[states.State] = []

    @property
    def colored_name(self):
        color = colors.CBLUE if self.team.number == 1 else colors.CRED
        return f"{color}{self.name}{colors.CEND}"

    @property
    def alive_team(self):
        return self.team.alive_heroes

    @property
    def is_team_alive(self):
        return len(self.alive_team) > 0

    def get_effects_dict(self):
        return {effect.name: effect for effect in self.effects}

    def get_states_dict(self):
        return {state.name: state for state in self.states}
    
    def get_state(self, state):
        if state.scaling:
            if state.name in self.states_names():
                old_state = list(filter(lambda old_state: old_state.name == state.name, self.states))[0]
                old_state.increase_moves(state.number_of_moves, self)
                state.on_getting(self)
                return

        self._add_state(state)
        state.on_getting(self)

    def _add_state(self, state):
        self.states.append(state)
        interface.print_msg(f'На {self.colored_name} упало состояние {state.colored_name}')
    
    def remove_state(self, state, interrupt=False):
        if not interrupt:
            state.on_ending(self)
        self.states.remove(state)
        interface.print_msg(f"Состояние {state.colored_name} на {self.colored_name} закончилось")

    def remove_effect_by_name(self, effect_name):
        effect = list(filter(lambda effect: effect.name == effect_name, self.effects))[0]
        self.remove_effect(effect)

    def effects_names(self):
        return [effect.name for effect in self.effects]
    
    def states_names(self):
        return [state.name for state in self.states]
    
    def get_effect(self, effect):
        effects_dict = self.get_effects_dict()
        if effect.name in effects_dict:
            effects_dict[effect.name].increase_value(effect.value, self)
        else:
            self.effects.append(effect)
            effect.check_on_max(self)

    def remove_effect(self, effect):
        self.effects.remove(effect)
        interface.print_msg(f"Эффект {effect.name} на {self.name} закончился")

    def add_rage(self, value):
        self.rage += value
        if self.rage > self.max_rage:
            self.rage = self.max_rage
        interface.print_msg(f"{self.name} ярость + {value}. Теперь у него(нее): {self.rage}")

    def take_rage(self, value):
        self.rage -= value
        if self.rage < 0:
            self.rage = 0
        interface.print_msg(f"{self.name} ярость - {value}. Теперь у него(нее): {self.energy}")

    def add_energy(self, value):
        self.energy += value
        if self.energy > self.max_energy:
            self.energy = self.max_energy
        interface.print_msg(f"{self.name} {ENERGY} + {value}. Теперь у него(нее): {self.energy}")

    def take_energy(self, value):
        self.energy -= value
        if self.energy < 0:
            self.energy = 0
        interface.print_msg(f"{self.name} {ENERGY} - {value}. Теперь у него(нее): {self.energy}")

    @staticmethod
    def filter_alive_heroes(heroes_list):
        return list(filter(lambda hero: hero.alive, heroes_list))

    def get_damage(self, damage):
        remaining_damage = damage - self.armor
        interface.print_msg(f"{self.colored_name} заблокировал {self.armor} урона. Прошло {remaining_damage}/{damage} урона.")
        if remaining_damage > 0:
            self.loose_hp(remaining_damage)

    def loose_hp(self, hp):
        self.hp -= hp
        interface.print_msg(f"{self.colored_name} потерял {hp} hp. Теперь у него {self.hp}/{self.max_hp} hp")
        self.check_is_alive()

    def check_is_alive(self):
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False
        interface.print_msg(f"{self.colored_name} погиб (ла)")

    def what_to_do_menu(self):
        pass

    def what_to_do(self):
        pass

    def make_move(self):
        interface.print_line()
        interface.print_msg(f"Ходит герой: {self.colored_name}")
        self.before_move()
        if not self.can_make_move:
            interface.print_msg('А нет, не ходит')
        else:
            if self.is_user_control:
                self.what_to_do_menu()
            else:
                self.what_to_do()
        self.after_move()
        interface.print_line()

    def tick_after_move_states(self):
        for state in self.states:
            state.after_move_tick(self)

    def tick_before_move_states(self):
        for state in self.states:
            state.before_move_tick(self)

    @classmethod
    def print_heroes(cls, heroes_list):
        for hero in heroes_list:
            print(hero)
            print('-' * 40 + "\n")

    def before_move(self):
        self.add_energy(3)
        self.can_make_move = self.can_use_skill = True
        self.tick_before_move_states()
    
    def after_move(self):
        self.tick_after_move_states()

    @property
    def short_str(self):
        return f"{self.colored_name}  ({self.hp}/{self.max_hp} HP) ({self.energy}/{self.max_energy} e)"

    def __str__(self):
        return f"{self.colored_name}  ({self.hp}/{self.max_hp})\n" \
               f"| сила={self.strength} | интеллект={self.mind} | магия={self.magic} |\n" \
               f"| броня={self.armor} | энергия={self.energy}/{self.max_energy} | ярость={self.rage}/{self.max_rage}\n" \
               f"{self.get_states_and_effects_str()}"

    def get_states_and_effects_str(self):
        text = "States:\n"
        for state in self.states:
            text += f"- {state}\n"
        text += 'Effects:\n'
        for effect in self.effects:
            text += f"- {effect}\n"
        return text

    def before_battle(self, enemy):
        self.enemy = enemy


class Mob(Hero):
    is_user_control = False
    reward = {

    }

    def what_to_do(self):
        pass


class Boss(Mob):
    pass


class Team:
    def __init__(self, number, heroes=None):
        self.number = number
        self.heroes: List[Hero] = heroes

    def add_hero(self, hero):
        self.heroes.append(hero)

    @property
    def alive_heroes(self):
        return list(filter(lambda hero: hero.alive, self.heroes))
