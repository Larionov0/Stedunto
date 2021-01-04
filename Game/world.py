from .Heroes import player
from .Heroes.Dop import skills
from .Locations.map import build_map, Place
import pickle

from .Tasks.Objects import start as start_tasks


class World:
    def __init__(self):
        map_ = build_map()

        player_ = player.Player(self)
        map_.places[0].add_hero(player_)
        player_.skills = list(map(lambda s_class: s_class(), skills.classes))
        self.data = {
            'map': map_,
            'player': player_,
            'Place': Place
        }

        self.stage = 1

        start_tasks.travelling_creator(self)
        start_tasks.first_blood_creator(self)

    @property
    def player(self):
        return self.data['player']
    
    @property
    def map(self):
        return self.data['map']
    
    def run(self):
        self.player.player_interface.menu_in_place()

    def save(self):
        with open('saving.dat', 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls):
        with open('saving.dat', 'rb') as file:
            return pickle.load(file)
