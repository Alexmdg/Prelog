from prelog.main import CheckLog
from prelog.main import LEVELS as poglevel
from prelog.main import FORMATS
from colorama import Fore


class Logger(CheckLog):
    def __init__(self):
        super().__init__(fmt=FORMATS['locate'])
        self.main.setLevel(poglevel['1'])
        self.display.setLevel(poglevel['1'])
        self.create_logger('client', Fore.CYAN, fmt=FORMATS['locate'])


log = Logger()


def hello(name):
    log.main.debug(f'Hello {name}')

