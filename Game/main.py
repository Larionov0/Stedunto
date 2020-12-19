from .Heroes import player
from .Heroes.Dop import skills
from .Actions.battle import HeroBattle
from .Actions.Battles.with_chert import battle
from os import system


system('cls')


player1 = player.Player()
player2 = player.Player()
player1.skills = list(map(lambda s_class: s_class(), skills.classes))
player2.skills = list(map(lambda s_class: s_class(), skills.classes))

battle()
input()
