import random


class InterfaceManager:
    _instance = None

    def __init__(self):
        self.instance = self

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance: InterfaceManager = cls()
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
                return 0
            if 0 < number <= len(lst):
                return number
            else:
                print('Ошибка с введенным числом')

    def check_chance(self, percent):
        return random.randint(1, 100) <= percent
