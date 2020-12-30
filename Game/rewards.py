from .Interface.interface import InterfaceManager
import random

interface = InterfaceManager.instance()


class Reward:
    def __init__(self, skill_cards=None, items=None, weapons=None, wears=None, coins=None, exp=None):
        self.skill_cards = skill_cards if skill_cards else []
        self.items = items if items else []
        self.weapons = weapons if weapons else []
        self.wears = wears if wears else []
        self.coins = coins if coins else []
        self.exp = exp if exp else 0

    def give_to_player(self, player):
        for skill in self.skill_cards:
            player.add_skill(skill)
        for item in self.items:
            pass
        for weapon in self.weapons:
            pass
        for wear in self.wears:
            pass
        if self.coins:
            if type(self.coins) is list:
                coins = random.randint(self.coins[0], self.coins[1])
                player.add_coins(coins)
            elif type(self.coins) is int:
                player.add_coins(self.coins)

        if self.exp:
            player.add_exp(self.exp)
