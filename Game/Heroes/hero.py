from typing import List
from .Dop import effects, states


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

    sex = 'М'
    enemy = None

    alive = True
    is_user_control = True

    can_use_skill = True
    can_make_move = True

    def __init__(self):
        self.team = [self]
        self.effects: List[effects.Effect] = []
        self.states: List[states.State] = []

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

        self.effects.append(state)
        state.on_getting(self)
    
    def remove_state(self, state, interrupt=False):
        if not interrupt:
            state.on_ending(self)
        self.effects.remove(state)
        print(f"Состояние {state.name} на {self.name} закончилось")

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
        print(f"Эффект {effect.name} на {self.name} закончился")

    def add_rage(self, value):
        self.rage += value
        if self.rage > self.max_rage:
            self.rage = self.max_rage
        print(f"{self.name} ярость + {value}. Теперь у него(нее): {self.rage}")

    def take_rage(self, value):
        self.rage -= value
        if self.rage < 0:
            self.rage = 0
        print(f"{self.name} ярость - {value}. Теперь у него(нее): {self.energy}")

    def add_energy(self, value):
        self.energy += value
        if self.energy > self.max_energy:
            self.energy = self.max_energy
        print(f"{self.name} енергия + {value}. Теперь у него(нее): {self.energy}")

    def take_energy(self, value):
        self.energy -= value
        if self.energy < 0:
            self.energy = 0
        print(f"{self.name} енергия - {value}. Теперь у него(нее): {self.energy}")

    @staticmethod
    def filter_alive_heroes(heroes_list):
        return list(filter(lambda hero: hero.alive, heroes_list))

    # def get_influence(self, specials: dict, states_list: list, effects_list: list):
    #     if 'damage' in specials:
    #         self.get_damage(specials['damage'])
    #     if 'magic_damage' in specials:
    #         self.loose_hp(specials['magic_damage'])
    # 
    #     for state in states_list:
    #         self.get_state(state)
    # 
    #     for effect in effects_list:
    #         self.get_effect(effect)

    def get_damage(self, damage):
        remaining_damage = damage - self.armor
        print(f"{self.name} заблокировал {self.armor} урона. Прошло {remaining_damage}/{damage} урона.")
        if remaining_damage > 0:
            self.loose_hp(remaining_damage)

    def loose_hp(self, hp):
        self.hp -= hp
        print(f"{self.name} потерял {hp} hp. Теперь у него {self.hp}/{self.max_hp}")
        self.check_is_alive()

    def check_is_alive(self):
        if self.hp <= 0:
            self.alive = False
            print(f"{self.name} die")

    def what_to_do_menu(self):
        pass

    def what_to_do(self):
        pass

    def make_move(self):
        print(f"Ходит герой: {self.name}")
        self.before_move()
        if not self.can_make_move:
            print('А нет, не ходит')
        else:
            if self.is_user_control:
                self.what_to_do_menu()
            else:
                self.what_to_do()
        self.after_move()

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
        return f"{self.name}  ({self.hp}/{self.max_hp} HP) ({self.energy}/{self.max_energy} e)"

    def __str__(self):
        return f"{self.name}  ({self.hp}/{self.max_hp})\n" \
               f"strength={self.strength} | mind={self.mind} | armor={self.armor} | magic={self.magic} | energy={self.energy}/{self.max_energy} | rage={self.rage}/{self.max_rage}\n" \
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


class Bot(Hero):
    is_user_control = False

    def what_to_do(self, enemy):
        pass

