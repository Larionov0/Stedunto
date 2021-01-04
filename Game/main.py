from os import system
from .world import World


system('cls')

saving = input('Загрузить? (y/n)')
if saving == 'y':
    World.load().run()
else:
    World().run()

input()
