from ..subtask import *
from ..task import *
from Game.rewards import Reward
from Game.Heroes.Heroes.goblin import Goblin


# ---
def f1(world):
    print('Бэн:\n'
          '     ой.. Я ж забыл ключи на мельнице.. Дурья башка...\n'
          '     Идем обратно, к мельнице')
    travel_to_melnitsa_creator(world)


def travel_to_sad_creator(world):
    player = world.player
    task = Task('Прогулка к саду', player, [], Reward(coins=2), 'Прогуляйтесь к Тыквенному саду', is_main=True,
                function=f1)
    task.add_subtask(
        TravelToPlaceSubTask(task, 'Доберись до тыквенного сада', world.map.get_place_by_xname('окраина:тыквенный сад'))
    )
    player.add_task(task)
    player.set_main_task(task)


# ---

def travel_to_melnitsa_creator(world):
    player = world.player
    task = Task('Прогулка к мельнице', player, [], Reward(coins=2), 'Вернись к мельнице', is_main=True)
    task.add_subtask(
        TravelToPlaceSubTask(task, 'Вернись к мельнице', world.map.get_place_by_xname('окраина:мельница'))
    )
    player.add_task(task)
    player.set_main_task(task)
