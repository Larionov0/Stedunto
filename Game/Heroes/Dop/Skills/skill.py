from Game.Interface.interface import InterfaceManager
from Game.Interface import colors

interface = InterfaceManager.instance()


class SkillCard:
    name = ''
    energy = 0
    freq = 0
    description = ''
    is_soft = False

    needed_hero_states = []
    needed_enemy_states = []

    def check_effects_on_player(self, player):
        result = True
        for state in self.needed_hero_states:
            if state not in player.states_names():
                result = False
                interface.print_msg(f"{colors.CRED}!{colors.CEND} У {player.colored_name} нету состояния {state}.")
        return result

    def calculate_needed_energy(self, player):
        if self.is_soft:
            return self.energy
        else:
            return self.energy + player.energy_penalty

    def cast(self, player, enemy):
        raise NotImplementedError

    def after_cast(self, player, enemy):
        self.player_remove_skill_from_arm(player)
        if self.is_soft:
            player.take_energy(self.energy)
        else:
            player.take_energy(self.energy + player.energy_penalty)
            player.increase_penalty()

    def player_remove_skill_from_arm(self, player):
        player.remove_skill_from_arm(self)

    def full_str(self):
        return

    def __str__(self):
        text = f"-|{self.name}|- ({self.energy})"
        return text

