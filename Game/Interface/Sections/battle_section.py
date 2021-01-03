from ..interface_interface import Interface
from ..interface import InterfaceManager
from .. import colors

interface = InterfaceManager.instance()


class BattleInterface(Interface):
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
                interface.start_menu()
                return
            elif choice == 's':
                self.choose_skill_menu()
            elif choice == 'i':
                self.print_info()
            elif choice == 'm':
                interface.start_menu()
                interface.show_messages()
            else:
                print('Не, не пойдет')

    def print_info(self):
        interface.start_menu()
        interface.print_msg('Герои:')
        for hero in self.player.alive_team + self.player.enemy.alive_team:
            interface.print_line()
            print(hero)
        interface.print_line()

    def choose_skill_menu(self):
        interface.start_menu()
        print('Выберите умение:')
        skill_card = interface.choose_one_from_list(self.player.arm)
        if skill_card is None:
            return
        self.cast_skill_menu(skill_card)

    def cast_skill_menu(self, skill):
        interface.start_menu()
        print(f"Вы выбрали умение: {skill}")
        print(skill.description)
        needed_energy = skill.energy + self.player.energy_penalty
        if self.player.energy < needed_energy:
            interface.print_msg(f"Ты не можешь кастонуть эту дичь из-за энергии ({self.player.energy}/{needed_energy})")
            return

        ans = input('Кастуем? (y/n): ')
        if ans == 'y':
            skill.cast(self.player, self.player.enemy)
        else:
            return
