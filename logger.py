# coding = utf-8
from datetime import datetime


class ConsoleColors:
    SUCCESS = '\033[32m'
    WARNING = '\033[93m'
    ERROR = '\033[31m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def info(msg):
    print(f'>> {get_time()}: {msg}')


def suc(msg):
    print(f'>> {get_time()}: {ConsoleColors.SUCCESS}{msg}{ConsoleColors.ENDC}')


def warn(msg):
    print(f'>> {get_time()}: {ConsoleColors.WARNING}{msg}{ConsoleColors.ENDC}')


def err(msg):
    print(f'>> {get_time()}: {ConsoleColors.ERROR}{msg}{ConsoleColors.ENDC}')


def fail(msg):
    print(f'>> {get_time()}: {ConsoleColors.FAIL}{msg}{ConsoleColors.ENDC}')
