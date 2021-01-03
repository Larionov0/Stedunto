from ..Interface.player_interface import InterfaceManager
from Game.globals import TRAVELLED_TO_PLACE_SIGNAL, HERO_BEATEN_SIGNAL
from ..Interface import colors as clr

interface = InterfaceManager.instance()


class SubTask:
    @property
    def signals(self):
        """
        Return: dict
            keys: SIGNALS (str)
            values: functions - checkers
        """
        return {}

    def __init__(self, task, short_description, function=None):
        self.task = task
        self.short_description = short_description
        self.function = function
        self.is_done = False

    def done(self):
        interface.print_msg(f'{clr.CYELLOW}Подзадание выполнено! ({self.short_description}){clr.CEND}')
        self.is_done = True
        self.on_stop()
        self.task.subtask_done()

    @property
    def player(self):
        return self.task.player

    def add_target_label(self):
        pass

    def on_start(self):
        pass

    def on_stop(self):
        pass


class TravelToPlaceSubTask(SubTask):
    @property
    def signals(self):
        return {
            TRAVELLED_TO_PLACE_SIGNAL: self.travelled_to_place_check
        }

    def __init__(self, task, short_description, place, function=None):
        super().__init__(task, short_description, function)
        self.place = place

    def travelled_to_place_check(self, place):
        if place == self.place:
            self.done()

    def on_start(self):
        self.player.target_place = self.place

    def on_stop(self):
        if self.player.main_task is self.task:
            self.player.target_place = None


class EnemyBeatenSubTask(SubTask):
    @property
    def signals(self):
        return {
            HERO_BEATEN_SIGNAL: self.hero_beaten_check
        }

    def __init__(self, task, short_description, hero, function=None):
        super().__init__(task, short_description, function)
        self.hero = hero

    def hero_beaten_check(self, hero):
        if hero == self.hero:
            self.done()

    def on_start(self):
        input('on_start')
        self.player.target_place = self.hero.place
        input(self.player.target_place)

    def on_stop(self):
        if self.player.main_task is self.task:
            self.player.target_place = None
