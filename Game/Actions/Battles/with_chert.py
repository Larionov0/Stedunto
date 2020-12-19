from Game.Heroes.Heroes.Bosses.chert import Chert
from Game.Heroes.Heroes.pervash import Pervash
from Game.Heroes.player import Player
from ..battle import HeroBattle


def battle():
    player = Player()
    for _ in range(100):
        p = Pervash(player.team)
        player.team.add_hero(p)

    HeroBattle.heroes_starts_battle(Chert(), player)
