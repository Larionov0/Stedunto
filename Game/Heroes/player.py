import random
from typing import List
from .Dop import colors, skills
from .hero import Hero
from ..Interface.interface import InterfaceManager

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

    def what_to_do_menu(self):
        while True:
            interface.enter()
            interface.clear()
            c1 = len(self.alive_team)
            c2 = len(self.enemy.alive_team)
            text = f"{colors.CBLUE}---= Меню действий героя =---{colors.CEND}\n" \
                   f"{self}\n" \
                   f"Ваши действия:\n" \
                   f"n - закончить ход\n" \
                   f"s - использовать умение\n" \
                   f"i - вывести всех героев ({colors.CBLUE}{c1}{colors.CEND} - {colors.CRED}{c2}{colors.CEND})\n" \
                   f"m - просмотреть последние сообщения\n" \
                   f"Ваш выбор: "
            choice = input(text)

            if choice == 'n':
                return
            elif choice == 's':
                self.choose_skill_menu(self.enemy)
            elif choice == 'i':
                self.print_info()
            elif choice == 'm':
                interface.show_messages()
            else:
                print('Не, не пойдет')

    def print_info(self):
        print(f'\n\n')
        print('Герои:')
        for hero in self.alive_team + self.enemy.alive_team:
            interface.print_line()
            print(hero)
        interface.print_line()

    def choose_skill_menu(self, enemy):
        print('Выберите умение:')
        number = interface.choose_one_from_list(self.arm)
        if number == 0:
            return
        skill = self.arm[number - 1]
        self.cast_skill_menu(enemy, skill)

    def cast_skill_menu(self, enemy, skill):
        interface.print_line()
        print(f"Вы выбрали умение: {skill}")
        print(skill.description)
        needed_energy = skill.energy + self.energy_penalty
        if self.energy < needed_energy:
            print(f"Ты не можешь кастонуть эту дичь из-за энергии ({self.energy}/{needed_energy})")
            return

        ans = input('Кастуем? (y/n): ')
        if ans == 'y':
            skill.cast(self, enemy)
        else:
            return

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

    def __str__(self):
        return super().__str__() + f"\nШтраф энергии:{self.energy_penalty}" + '\n' + self.get_skills_str()

