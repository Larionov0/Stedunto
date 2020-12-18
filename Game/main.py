from .Heroes import player
from .Heroes.Dop import skills
from .Actions.battle import HeroBattle


player1 = player.Player()
player2 = player.Player()
player1.skills = list(map(lambda s_class: s_class(), skills.classes))
player2.skills = list(map(lambda s_class: s_class(), skills.classes))

HeroBattle.heroes_starts_battle(player1, player2)
