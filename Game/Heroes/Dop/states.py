class State:
    name = 'State'
    scaling = True

    def __init__(self, number_of_moves):
        self.number_of_moves = number_of_moves

    def decrease_moves(self, hero):
        self.number_of_moves -= 1
        print(f"Осталось {self.number_of_moves} ходов для эффекта {self.name} на герое {hero.name}")
        if self.number_of_moves == 0:
            hero.remove_effect(self)
            self.on_ending(hero)

    def increase_moves(self, moves, hero):
        self.number_of_moves += moves
        print(f"Осталось {self.number_of_moves} ходов для эффекта {self.name} на герое {hero.name} (+{moves})")

    def on_getting(self, hero):
        pass

    def before_move_tick(self, hero):
        pass

    def after_move_tick(self, hero):
        pass

    def on_ending(self, hero):
        pass

    def __str__(self):
        return f"<{self.name}> ({self.number_of_moves})"


class Stun(State):
    name = 'оглушение'

    def before_move_tick(self, hero):
        print(f"Герой {hero.name} оглушен и не может совершить ход")
        hero.can_make_move = False
        self.decrease_moves(hero)


class Bleeding(State):
    name = 'кровотечение'

    value = 5

    def after_move_tick(self, hero):
        print(f"Кровотечение у {self.name}\n")
        hero.loose_hp(self.value)
        self.decrease_moves(hero)


class Soaking(State):
    name = 'промокание'

    def after_move_tick(self, hero):
        print(f'Промокший и устаешь сильней:)')
        hero.take_energy(1)
        self.decrease_moves(hero)


class Fallen(State):
    name = "упавший"

    def on_getting(self, hero):
        print(f"{hero.name} упал на {self.number_of_moves} ходов")

    def after_move_tick(self, hero):
        print(f'{hero.name} еще валяется')
        self.decrease_moves(hero)

    def on_ending(self, hero):
        print(f"{hero.name} потрудился встать")
        hero.take_energy(2)


class TurnedAround(State):
    name = "развернут"

    def on_getting(self, hero):
        print(f"{hero.name} развернулся на {self.number_of_moves} ходов")

    def after_move_tick(self, hero):
        self.decrease_moves(hero)
