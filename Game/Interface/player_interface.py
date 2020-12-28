from .interface import InterfaceManager
from . import colors
from Game.Locations.dijkstra import SuperDijkstra

interface = InterfaceManager.instance()


class PlayerInterface:
    def __init__(self, player):
        self.player = player

    def what_to_do_menu(self):
        while True:
            interface.start_menu()
            c1 = len(self.player.alive_team)
            c2 = len(self.player.enemy.alive_team)
            text = f"{colors.CBLUE}---= Меню действий героя =---{colors.CEND}\n" \
                   f"{self.player}\n" \
                   f"Ваши действия:\n" \
                   f"n - закончить ход\n" \
                   f"s - использовать умение\n" \
                   f"i - вывести всех героев ({colors.CBLUE}{c1}{colors.CEND} - {colors.CRED}{c2}{colors.CEND})\n" \
                   f"m - просмотреть последние сообщения\n" \
                   f"Ваш выбор: "
            choice = interface.press(text)

            if choice == 'n':
                return
            elif choice == 's':
                self.choose_skill_menu()
            elif choice == 'i':
                self.print_info()
            elif choice == 'm':
                interface.show_messages()
            else:
                print('Не, не пойдет')

    def print_info(self):
        print(f'\n\n')
        print('Герои:')
        for hero in self.player.alive_team + self.player.enemy.alive_team:
            interface.print_line()
            print(hero)
        interface.print_line()

    def choose_skill_menu(self):
        print('Выберите умение:')
        skill_card = interface.choose_one_from_list(self.player.arm)
        if skill_card is None:
            return
        self.cast_skill_menu(skill_card)

    def cast_skill_menu(self, skill):
        interface.print_line()
        print(f"Вы выбрали умение: {skill}")
        print(skill.description)
        needed_energy = skill.energy + self.player.energy_penalty
        if self.player.energy < needed_energy:
            print(f"Ты не можешь кастонуть эту дичь из-за энергии ({self.player.energy}/{needed_energy})")
            return

        ans = input('Кастуем? (y/n): ')
        if ans == 'y':
            skill.cast(self.player, self.player.enemy)
        else:
            return

    # ---- locations
    def menu_in_place(self):
        while True:
            interface.start_menu()
            print(f'---= Вы находитесь в {self.player.place} =---\n{self.base_player_info()}')
            print(self.player.target_place)
            print('i - инвентарь')
            print('m - переместиться')
            print('h - взаимодействие с персонажами')
            print('t - мои задания')

            choice = interface.press('Ваш выбор: ')
            if choice == 'i':
                pass
            elif choice == 'm':
                self.move_menu()
            elif choice == 'h':
                pass
            elif choice == 't':
                self.my_tasks_menu()
            else:
                print('Не пойдет :(')

    def tasks_str(self, tasks):
        text = ''
        for task_str in self.tasks_list_str(tasks):
            text += f"- {task_str}\n"
        return text

    def tasks_list_str(self, tasks):
        return list(map(
            lambda task: f"{task.short_str + (f'{colors.CYELLOW}(*){colors.CEND}' if task == self.player.main_task else '')}",
            tasks
        ))

    def my_tasks_menu(self):
        while True:
            interface.start_menu()
            text = '---= Мои Задания =---\n' \
                   f'Основные: \n{self.tasks_str(self.player.main_tasks)}\n' \
                   f'Дополнительные:\n{self.tasks_str(self.player.secondary_tasks)}\n'
            text += '\nВыберите раздел:\n' \
                    '0 - назад\n' \
                    '1 - основные\n' \
                    '2 - дополнительные'
            print(text)
            choice = interface.press('Ваш выбор: ')
            if choice == '1':
                self.my_concrete_tasks_menu(True)
            elif choice == '2':
                self.my_concrete_tasks_menu(False)
            elif choice == '0':
                return

    def my_concrete_tasks_menu(self, is_main):
        if is_main:
            tasks = self.player.main_tasks
        else:
            tasks = self.player.secondary_tasks

        while True:
            interface.start_menu()
            if is_main:
                print('---= Основные задания =---')
            else:
                print('---= Второстепенные задания =---')

            index = interface.choose_one_index_from_list(self.tasks_list_str(tasks))
            if index is None:
                return
            task = tasks[index]
            self.task_menu(task)

    def task_menu(self, task):
        while True:
            interface.start_menu()
            text = '---= Меню задания =---\n' \
                   f'Выбрано задание:\n{task}\n' \
                   f'0 - назад\n' \
                   f'1 - назначить сие задание главным\n' \
                   f'2 - считерить сие задание\n'
            print(text)
            choice = interface.press('Ваш выбор: ')
            if choice == '1':
                self.player.set_main_task(task)
                interface.print_msg('Задание очень успешно назначено')
            elif choice == '2':
                interface.print_msg('Я те щяс как считерю. Играй давай нормально.')
            elif choice == '0':
                return

    def get_adjacent_places_str_list(self, places):
        """
        return: list of str
        Every str is place short str but with (*) on target place.
        """
        check = False
        if self.player.target_place:
            dijkstra = SuperDijkstra.get_instance()
            way = dijkstra.find_shortest_way(self.player.place, self.player.target_place)
            places_list = way.places_list
            if len(places_list) > 1:
                next_place = way.places_list[1]
                check = True

        return list(map(
            lambda place: str(place) + (f' {colors.CYELLOW}*{colors.CEND}' if check and place == next_place else ''),
            places
        ))

    def move_menu(self):
        interface.start_menu()
        print('-----= Перемещение =-----')

        interface.print_msg(f'Вы находитесь тут: {self.player.place}')
        places = self.player.place.adjacent_places_list
        l = self.get_adjacent_places_str_list(places)
        index = interface.choose_one_index_from_list(l)
        if index is None:
            return
        place = places[index]

        self.player.move_to_place(place)
        return

    def base_player_info(self):
        player = self.player
        text = f"Герой {player.name}\n" \
               f"hp: {player.hp}/{player.max_hp}\n"
        if player.main_task:
            text += f"Задание: {player.main_task.short_str}"
        return text
