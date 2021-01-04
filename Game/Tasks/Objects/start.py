from ..subtask import *
from ..task import *
from Game.rewards import Reward
from Game.Locations.place import Place
from Game.Heroes.Heroes.goblin import Goblin


def travelling_creator(world):
    def after_travel(world):
        place = world.map.get_place_by_name('Тропа')
        place.add_hero(
            Goblin()
        )
        interface.print_msg('Гоблин появился')

    player = world.player
    task = Task('Прогулка', player, [], Reward(coins=10), function=after_travel)
    task.add_subtask(
        TravelToPlaceSubTask(task, 'Доберись до аудиторной', Place.get_place_by_name('Аудиторная'))
    )
    task.add_subtask(
        TravelToPlaceSubTask(task, 'Доберись до Зарослей', Place.get_place_by_name('Заросли'))
    )
    player.add_task(task)


def first_blood_creator(world):
    player = world.player
    task = Task('Первая кровь', player, [], Reward(coins=20))
    task.add_subtask(
        EnemyBeatenSubTask(task, 'Убей гоблина', Place.get_place_by_name('Заросли').heroes[0])
    )
    player.add_task(task)
