from Game.Interface.interface import InterfaceManager

interface = InterfaceManager.instance()


class SkillCard:
    name = ''
    energy = 0
    freq = 0
    description = ''

    needed_hero_states = []
    needed_enemy_states = []

    def check_effects_on_player(self, player):
        result = True
        for state in self.needed_hero_states:
            if state not in player.states_names():
                result = False
                interface.print_msg(f"У {self.name} нету состояния {state}.")
        return result

    def cast(self, player, enemy):
        raise NotImplementedError

    def after_cast(self, player, enemy):
        player.take_energy(self.energy + player.energy_penalty)
        self.player_remove_skill_from_arm(player)
        player.increase_penalty()

    def player_remove_skill_from_arm(self, player):
        player.remove_skill_from_arm(self)

    def full_str(self):
        return

    def __str__(self):
        text = f"-|{self.name}|- ({self.energy})"
        return text

