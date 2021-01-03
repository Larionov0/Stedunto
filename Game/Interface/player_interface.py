from .interface import InterfaceManager
from . import colors
from Game.Locations.dijkstra import SuperDijkstra
from .Sections.tasks_section import TasksInterface
from .Sections.battle_section import BattleInterface
from .interface_interface import Interface
from Game.Actions.battle import HeroBattle
from Game.globals import *

interface = InterfaceManager.instance()


class PlayerInterface(Interface):
    def __init__(self, player):
        super().__init__(player)
        self.tasks_interface = TasksInterface(self.player)
        self.battle_interface = BattleInterface(self.player)

    def what_to_do_menu(self):
        return self.battle_interface.what_to_do_menu()

    def menu_in_place(self):
        while True:
            interface.start_menu()
            print(f'---= Вы находитесь в {self.player.place} =---\n{self.base_player_info()}')
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
                self.interaction_with_heroes()
            elif choice == 't':
                self.tasks_interface.my_tasks_menu()
            else:
                print('Не пойдет :(')

    def interaction_with_heroes(self):
        while True:
            interface.start_menu()
            text = '----= Взаимодействие с персонажами =----\n' \
                   'Выберите персонажа для взаимодействия:'
            print(text)
            heroes = list(filter(lambda hero: hero is not self.player, self.player.place.heroes))
            hero = interface.choose_one_from_list(heroes, short_str=True)
            if hero is None:
                return
            return self.what_to_do_with_hero(hero)

    def what_to_do_with_hero(self, hero):
        interface.menu(
            f'Взаимодействие с персонажем {hero.name}',
            f'{hero}\nКак взаимодействуем:',
            {
                'b': ['начать бой', lambda: self.start_battle(hero)],
                't': ['поговорить', lambda: self.start_talking(hero)]
            },
            return_back=False
        )

    def start_battle(self, enemy):
        winner = HeroBattle.heroes_starts_battle(self.player, enemy)
        if winner is self.player:
            self.player.win_battle(enemy)
        else:
            interface.print_msg('Вы погибли:(')
            interface.enter()

    def start_talking(self, hero):
        interface.print_msg(f"{hero.colored_name}: Нахуй ты со мной говоришь, я персонаж массовки.\n"
                            f"А теперь отойди, и не мешай этому элементу интерьера втыкать в одну точку.\n"
                            f"Так надо.")

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

        print(f'Вы находитесь тут: {self.player.place}')
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
               f"hp: {player.hp}/{player.max_hp}\n" \
               f"Монеты: {player.coins}\n"
        if player.main_task:
            text += f"Задание: {player.main_task.short_str}"
        return text
