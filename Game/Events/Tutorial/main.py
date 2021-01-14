from Game.Interface.interface import InterfaceManager
from Game.Tasks.Objects.start import travel_to_sad_creator

interface = InterfaceManager.instance()
FOLDER = 'Game/Events/Tutorial'


def get_text(filename):
    with open(FOLDER + "/" + filename, encoding='utf-8') as file:
        text = file.read()
    return text


def tutorial_event(world):
    text = get_text('tutorial_start.txt')
    print(text)
    interface.choose_one_from_list(['чего', "кого", "какого"], on_zero=False)
    print(get_text('2.txt'))
    name = input('Ваше имя: ')
    world.player.name = name
    print('Но прежде всего тебе стоит научиться ходить.\n'
          'Давай так, встретимся с тобой в тыквенном саду!')
    travel_to_sad_creator(world)
