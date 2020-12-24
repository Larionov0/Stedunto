from .Heroes import player
from .Heroes.Dop import skills
from .Actions.battle import HeroBattle
from .Actions.Battles.with_chert import battle
from .Locations.map import build_map
from os import system


system('cls')

map_ = build_map()

player1 = player.Player()
map_[0].add_hero(player1)
player1.skills = list(map(lambda s_class: s_class(), skills.classes))
player1.player_interface.menu_in_place()

input()
