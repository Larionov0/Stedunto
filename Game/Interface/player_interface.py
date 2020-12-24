from .interface import InterfaceManager
from . import colors

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
            choice = input(text)

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
            print(f'---= Вы находитесь в {self.player.place} =---')
            print('i - инвентарь')
            print('l - переместиться')
            choice = input('Ваш выбор: ')
            if choice == 'i':
                pass
            elif choice == 'l':
                self.move_menu()
            else:
                print('Не пойдет :(')

    def move_menu(self):
        interface.start_menu()
        print('-----= Перемещение =-----')
        interface.print_msg(f'Вы находитесь тут: {self.player.place}')
        place = interface.choose_one_from_list(self.player.place.adjacent_places_list)
        if place is None:
            return

        self.player.move_to_place(place)
        return
