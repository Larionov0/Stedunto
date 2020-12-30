from ..interface_interface import Interface
from ..interface import InterfaceManager
from .. import colors

interface = InterfaceManager.instance()


class TasksInterface(Interface):
    def tasks_str(self, tasks):
        text = ''
        for task_str in self.tasks_list_str(tasks):
            text += f"- {task_str}\n"
        return text

    def tasks_list_str(self, tasks):
        return list(map(
            lambda
                task: f"{task.short_str + (f'{colors.CYELLOW}(*){colors.CEND}' if task == self.player.main_task else '')}",
            tasks
        ))

    def my_tasks_menu(self):
        while True:
            interface.start_menu()
            text = '---= Мои Задания =---\n' \
                   f'Основные: \n{self.tasks_str(self.player.main_tasks)}\n' \
                   f'Дополнительные:\n{self.tasks_str(self.player.secondary_tasks)}\n'
            text += '\nВыберите раздел:\n' \
                    '0 - назад\n' \
                    '1 - основные\n' \
                    '2 - дополнительные'
            print(text)
            choice = interface.press('Ваш выбор: ')
            if choice == '1':
                self.my_concrete_tasks_menu(True)
            elif choice == '2':
                self.my_concrete_tasks_menu(False)
            elif choice == '0':
                return

    def my_concrete_tasks_menu(self, is_main):
        if is_main:
            tasks = self.player.main_tasks
        else:
            tasks = self.player.secondary_tasks

        while True:
            interface.start_menu()
            if is_main:
                print('---= Основные задания =---')
            else:
                print('---= Второстепенные задания =---')

            index = interface.choose_one_index_from_list(self.tasks_list_str(tasks))
            if index is None:
                return
            task = tasks[index]
            self.task_menu(task)

    def task_menu(self, task):
        while True:
            interface.start_menu()
            text = '---= Меню задания =---\n' \
                   f'Выбрано задание:\n{task}\n' \
                   f'0 - назад\n' \
                   f'1 - назначить сие задание главным\n' \
                   f'2 - считерить сие задание\n'
            print(text)
            choice = interface.press('Ваш выбор: ')
            if choice == '1':
                self.player.set_main_task(task)
                interface.print_msg('Задание очень успешно назначено')
            elif choice == '2':
                interface.print_msg('Я те щяс как считерю. Играй давай нормально.')
            elif choice == '0':
                return
