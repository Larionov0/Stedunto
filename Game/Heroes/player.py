import random
from typing import List, Optional
from .Dop import colors, skills
from .hero import Hero
from ..Interface.interface import InterfaceManager
from ..Interface.player_interface import PlayerInterface
from ..Tasks.task import Task
from Game import globals
from Game.Actions.battle import HeroBattle

interface = InterfaceManager.instance()


class Player(Hero):
    name = 'Леха'
    hp = max_hp = 100
    armor = 1
    fighting = 10
    strength = 10
    energy = max_energy = 10
    magic = 0
    coins = 10

    _standard_team_number = 1

    max_arm_length = 10

    energy_penalty = 0

    def __init__(self, world):
        super().__init__()
        self.skills: List[skills.SkillCard] = []
        self.arm: List[skills.SkillCard] = []
        self.player_interface = PlayerInterface(self)
        self.target_place = None

        self.tasks: List[Task] = []
        self.main_task: Optional[Task] = None

        self.world = world

    def add_coins(self, coins):
        self.coins += coins
        interface.print_msg(f"{colors.CYELLOW}{self.name} получил {coins} монет!{colors.CEND}")

    def take_coins(self, coins):
        pass

    def add_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)
            interface.print_msg(f'{self.colored_name} получил карту умения!!!\n{skill}')

    def add_task(self, task):
        self.tasks.append(task)
        interface.print_msg(f"{colors.CYELLOW}У тебя новое задание: {task.name}{colors.CEND}")

    def set_main_task(self, task):
        if self.main_task:
            self.main_task.stop()
        self.main_task = task
        self.main_task.start()

    @property
    def alive_tasks(self):
        return list(filter(lambda task: not task.is_done, self.tasks))

    @property
    def main_tasks(self):
        return list(filter(lambda task: task.is_main, self.alive_tasks))

    @property
    def secondary_tasks(self):
        return list(filter(lambda task: not task.is_main, self.alive_tasks))

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
        interface.start_menu()
        interface.print_msg('Начинается битва')
        super().before_battle(enemy)
        for _ in range(4):
            self.pick_up_cards()

    def start_battle(self, enemy):
        winner = HeroBattle.heroes_starts_battle(self, enemy)
        if winner is self:
            self.win_battle(enemy)
        else:
            interface.print_msg('Вы погибли:(')
            interface.enter()

    def win_battle(self, enemy):
        for enemy_ in enemy.team.heroes:
            print(f'{colors.CYELLOW}Ваша награда за {enemy_.short_str}{colors.CEND}')
            enemy_.reward.give_to_player(self)

            self.check_all_tasks(globals.HERO_BEATEN_SIGNAL, hero=enemy_)

    def move_to_place(self, place):
        self.place.remove_hero(self)
        place.add_hero(self)
        interface.print_msg(f'{colors.CGREEN}{self.name} переместился в {place}{colors.CEND}')

        self.check_all_tasks(globals.TRAVELLED_TO_PLACE_SIGNAL, place=place)

        aggressive_enemies_team = place.player_came_here(self)  # check if some mobs attacks player
        if aggressive_enemies_team.heroes:
            self.start_battle(aggressive_enemies_team.alive_heroes[0])

    def main_task_check(self, signal, *args, **kwargs):
        if self.main_task:
            self.main_task.check(signal, *args, **kwargs)

    def check_all_tasks(self, signal, *args, **kwargs):
        for task in self.alive_tasks:
            task.check(signal, *args, **kwargs)

    def __str__(self):
        return super().__str__() + f"\nШтраф энергии:{self.energy_penalty}" + '\n' + self.get_skills_str()

