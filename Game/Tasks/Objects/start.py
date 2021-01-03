from ..subtask import *
from ..task import *
from Game.rewards import Reward
from Game.Locations.place import Place


def travelling_creator(player):
    task = Task('Прогулка', player, [], Reward(coins=10))
    task.add_subtask(
        TravelToPlaceSubTask(task, 'Доберись до аудиторной', Place.get_place_by_name('Аудиторная'))
    )
    task.add_subtask(
        TravelToPlaceSubTask(task, 'Доберись до Зарослей', Place.get_place_by_name('Заросли'))
    )
    player.add_task(task)


def first_blood_creator(player):
    task = Task('Первая кровь', player, [], Reward(coins=20))
    task.add_subtask(
        EnemyBeatenSubTask(task, 'Убей гоблина', Place.get_place_by_name('Заросли').heroes[0])
    )
    player.add_task(task)
