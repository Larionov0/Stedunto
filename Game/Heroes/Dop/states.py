from Game.Interface import colors
from Game.Interface.interface import InterfaceManager

interface = InterfaceManager.instance()


class State:
    name = 'State'
    scaling = False
    color = colors.CEND
    is_alive = True

    @property
    def colored_name(self):
        return f"{self.color}{self.name}{colors.CEND}"

    def on_getting(self, hero):
        pass

    def before_move_tick(self, hero):
        pass

    def after_move_tick(self, hero):
        pass

    def on_ending(self, hero):
        pass

    def die(self, hero):
        hero.remove_state(self)
        self.is_alive = False

    def __str__(self):
        return f"<{self.colored_name}>"


class CountdownState(State):
    scaling = True

    def __init__(self, number_of_moves):
        self.number_of_moves = number_of_moves

    def decrease_moves(self, hero):
        self.number_of_moves -= 1
        print(f"Осталось {self.number_of_moves} ходов для эффекта {self.colored_name} на герое {hero.colored_name}")
        if self.number_of_moves == 0:
            self.die(hero)

    def increase_moves(self, moves, hero):
        self.number_of_moves += moves
        print(f"Осталось {self.number_of_moves} ходов для состояния "
              f"{self.colored_name} на герое {hero.colored_name} (+{moves})")

    def __str__(self):
        return f"<{self.colored_name}> ({self.number_of_moves})"


class Stun(CountdownState):
    name = 'оглушение'
    color = colors.CGREY

    def before_move_tick(self, hero):
        print(f"Герой {hero.name} оглушен и не может совершить ход")
        hero.can_make_move = False
        self.decrease_moves(hero)


class Bleeding(CountdownState):
    name = 'кровотечение'
    color = colors.CRED2

    value = 5

    def after_move_tick(self, hero):
        interface.print_line()
        print(f"{self.colored_name} у {hero.colored_name}")
        hero.loose_hp(self.value)
        self.decrease_moves(hero)
        interface.print_line()


class Soaking(CountdownState):
    name = 'промокание'
    color = colors.CBLUE2

    def after_move_tick(self, hero):
        print(f'Промокший и устаешь сильней:)')
        hero.take_energy(1)
        self.decrease_moves(hero)


class Fallen(CountdownState):
    name = "упавший"
    color = colors.CYELLOW

    def on_getting(self, hero):
        print(f"{hero.name} упал на {self.number_of_moves} ходов")

    def after_move_tick(self, hero):
        print(f'{hero.name} еще валяется')
        self.decrease_moves(hero)

    def on_ending(self, hero):
        print(f"{hero.name} потрудился встать")
        hero.take_energy(2)


class TurnedAround(CountdownState):
    name = "развернут"
    color = colors.CYELLOW

    def on_getting(self, hero):
        interface.print_msg(f"{hero.name} развернулся на {self.number_of_moves} ходов")

    def after_move_tick(self, hero):
        self.decrease_moves(hero)


class Ready(CountdownState):
    name = 'готовность'
    color = colors.CGREEN

    def on_getting(self, hero):
        interface.print_msg(f'{hero.colored_name} в состоянии готовности на {self.number_of_moves} ходов')

    def after_move_tick(self, hero):
        self.decrease_moves(hero)


class Burning(State):
    name = 'горение'
    color = colors.CRED2
    scaling = False

    def __init__(self, power):
        self.power = power

    def on_getting(self, hero):
        interface.print_msg(f'{hero.colored_name} был подожжен с силой {self.power}')

    def after_move_tick(self, hero):
        interface.print_line()
        interface.print_msg(f'{self.colored_name} в деле')
        hero.get_damage(self.power)
        self.decrease_power(hero)
        interface.print_line()

    def decrease_power(self, hero):
        self.power -= 2
        if self.power <= 0:
            self.die(hero)

    def __str__(self):
        return super().__str__() + f' ({self.power})'
