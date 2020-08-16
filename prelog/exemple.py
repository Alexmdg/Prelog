from prelog.main import CheckLog
from prelog.main import LEVELS as poglevel


log = CheckLog()


def hello(name):
    log.main.debug(f'Hello {name}')

