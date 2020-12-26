from ..Interface.player_interface import InterfaceManager
from ..Interface import colors
from .subtask import SubTask
from typing import List

interface = InterfaceManager.instance()


class Task:
    def __init__(self, name, player, subtasks, reward, description=''):
        self.player = player
        self.name = name
        self.subtasks: List[SubTask] = subtasks
        self.reward = reward
        self.description = description
        self.cur_subtask_index = 0
        self.is_done = False

    def start(self):
        self.cur_subtask.on_start()

    def stop(self):
        self.cur_subtask.on_stop()

    def subtask_done(self):
        self.cur_subtask_index += 1
        if self.cur_subtask_index == self.subtasks_count:
            self.done()
        else:
            self.cur_subtask.on_start()

    @property
    def subtasks_count(self):
        return len(self.subtasks)

    @property
    def cur_subtask(self):
        return self.subtasks[self.cur_subtask_index]

    def done(self):
        interface.print_msg(f'{colors.CYELLOW}Задание {self.name} выполнено!!!{colors.CEND}')
        self.give_reward()
        self.is_done = True
        self.player.main_task = None

    def give_reward(self):
        interface.print_msg('Ваша награда:')

    def check(self, signal, *args, **kwargs):
        if signal in self.cur_subtask.signals:
            checker = self.cur_subtask.signals[signal]
            checker(*args, **kwargs)

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)

    @property
    def short_str(self):
        return f"{self.name} (выполняется {self.subtasks[self.cur_subtask_index].short_description})"

    def __str__(self):
        start = f"Задание {self.name}"
        if self.is_done:
            start += "(done)"
        text = start + f'\n{self.description}'
        for i in range(self.cur_subtask_index + 1):
            text += f"- {self.subtasks[i].short_description}\n"

        return text
