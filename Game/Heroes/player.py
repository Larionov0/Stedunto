import random
from typing import List
from .Dop import colors, skills
from .hero import Hero
from ..Interface.interface import InterfaceManager
from ..Interface.player_interface import PlayerInterface

interface = InterfaceManager.instance()


class Player(Hero):
    name = 'Леха'
    hp = max_hp = 100
    armor = 1
    fighting = 10
    strength = 10
    energy = max_energy = 10
    magic = 0

    _standard_team_number = 1

    max_arm_length = 10

    energy_penalty = 0

    def __init__(self):
        super().__init__()
        self.skills: List[skills.SkillCard] = []
        self.arm: List[skills.SkillCard] = []
        self.player_interface = PlayerInterface(self)

    def what_to_do_menu(self):
        self.player_interface.what_to_do_menu()

    def get_skills_str(self):
        text = "Умения:\n"
        for skill in self.arm:
            text += f'- {skill}\n'
        return text

    def add_skill_to_arm(self, skill):
        if len(self.arm) != self.max_arm_length:
            self.arm.append(skill)
            interface.print_msg(f"{self.name} получил карту умения: {skill}")

    def remove_skill_from_arm(self, skill):
        self.arm.remove(skill)

    def before_move(self):
        self.energy_penalty = 0
        self.pick_up_cards()
        super().before_move()

    def increase_penalty(self):
        self.energy_penalty += 1

    def pick_up_cards(self, n=1):
        for _ in range(n):
            skill_card = self.get_card_by_freq()
            self.add_skill_to_arm(skill_card)

    def get_card_by_freq(self):
        if self.skills:
            skill_card = random.choices(self.skills, [skill.freq for skill in self.skills])[0]
        else:
            return
        return skill_card

    def die(self):
        super().die()
        print(f'{colors.CRED2}Вы погибли{colors.CEND}')
        interface.enter()

    def before_battle(self, enemy):
        super().before_battle(enemy)
        for _ in range(4):
            self.pick_up_cards()

    def move_to_place(self, place):
        self.place.remove_hero(self)
        place.add_hero(self)
        interface.print_msg(f'{colors.CGREEN}{self.name} переместился в {place}{colors.CEND}')

    def __str__(self):
        return super().__str__() + f"\nШтраф энергии:{self.energy_penalty}" + '\n' + self.get_skills_str()
