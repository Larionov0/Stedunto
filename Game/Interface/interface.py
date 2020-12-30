import random
from os import system
import msvcrt


class InterfaceManager:
    _instance = None
    messages_limit = 50

    def __init__(self, osoznanno=False):
        if not osoznanno:
            raise Exception('Неосознанный выбор!')
        InterfaceManager._instance = self
        self.messages = []
        self.new_messages = False

    def press(self, text):
        print(text)
        try:
            return msvcrt.getch().decode()
        except:
            return ''

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance: InterfaceManager = cls(osoznanno=True)
        return cls._instance

    @staticmethod
    def print_line(n=40):
        print('-'*n)

    @staticmethod
    def input_int(text, error_message='Не целое число'):
        while True:
            ans = input(text)
            if ans.isdigit():
                return int(ans)
            else:
                print(error_message)

    def choose_one_from_list(self, lst, on_zero='отмена', short_str=False):
        index = self.choose_one_index_from_list(lst, on_zero, short_str)
        if index is None:
            return None
        return lst[index]

    def choose_one_index_from_list(self, lst, on_zero='отмена', short_str=False):
        while True:
            if on_zero:
                print(f'0 - {on_zero}')
            for i, el in enumerate(lst):
                if short_str:
                    print(f"{i + 1} - {el.short_str}")
                else:
                    print(f"{i + 1} - {el}")
            number = self.input_int('Ваш выбор: ')
            if number == 0 and on_zero:
                return None
            if 0 < number <= len(lst):
                return number-1
            else:
                print('Ошибка с введенным числом')

    def check_chance(self, percent):
        return random.randint(1, 100) <= percent

    def print_msg(self, text):
        print(text)
        self.add_message(text)
        self.new_messages = True

    def add_message(self, text):
        self.messages.insert(0, text)
        while len(self.messages) > self.messages_limit:
            self.messages.pop()

    def show_messages(self):
        print('\n--= Последние сообщения =--')
        for message in self.messages:
            print('- - - -')
            print(message)
        print('- - - -')

    def start_menu(self):
        if self.new_messages:
            self.enter()
        self.clear()
        self.new_messages = False

    def enter(self):
        input('\npress <Enter>')

    def clear(self):
        system('cls')

    def menu(self, header, text, variants_dict, input_text='Ваш выбор:', on_zero='назад'):
        """
        variants_dict:
        {
            'a': ['атаковать', lambda : self.attack_menu(enemy)],
            'b': ['защищаться', self.def_menu]
        }
        """
        while True:
            self.start_menu()
            print(f'----= {header} =-----')
            print(text)
            if on_zero:
                print(f'0 - {on_zero}')
            for variant in variants_dict:
                print(f'{variant} - {variants_dict[variant][0]}')
            choice = self.press(input_text)
            if on_zero and choice == '0':
                return
            if choice in variants_dict:
                variants_dict[choice][1]()
