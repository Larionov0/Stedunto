from .Heroes import player
from .Heroes.Dop import skills
from .Actions.battle import HeroBattle
from .Actions.Battles.with_chert import battle
from .Locations.map import build_map, Place
from os import system
from .Tasks.task import Task
from .Tasks.subtask import *


system('cls')

map_ = build_map()

player1 = player.Player()
map_[0].add_hero(player1)
player1.skills = list(map(lambda s_class: s_class(), skills.classes))

data = {
    'map': map_,
    'player': player1
}


task = Task('Прогулка', player1, [], None)
task.add_subtask(
    TravelToPlaceSubTask(task, 'Доберись до аудиторной', Place.get_place_by_name('Аудиторная'))
)
task.add_subtask(
    TravelToPlaceSubTask(task, 'Доберись до Зарослей', Place.get_place_by_name('Заросли'))
)

task2 = Task('Отгулка', player1, [], None)
task2.add_subtask(
    TravelToPlaceSubTask(task2, 'Идем к Опушке', Place.get_place_by_name('Опушка'))
)

player1.add_task(task)
player1.add_task(task2)
player1.set_main_task(task)

player1.player_interface.menu_in_place()

input()
