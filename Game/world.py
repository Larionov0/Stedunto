from .Heroes import player
from .Heroes.Dop import skills
from .Locations.map import build_map, Place

from .Tasks.Objects import start as start_tasks


class World:
    def __init__(self):
        map_ = build_map()

        player_ = player.Player(self)
        map_[0].add_hero(player_)
        player_.skills = list(map(lambda s_class: s_class(), skills.classes))
        self.data = {
            'map': map_,
            'player': player_
        }

        start_tasks.travelling_creator(player_)
        start_tasks.first_blood_creator(player_)
        
        self.stage = 1
    
    @property
    def player(self):
        return self.data['player']
    
    @property
    def map(self):
        return self.data['map']
    
    def run(self):
        self.player.player_interface.menu_in_place()
