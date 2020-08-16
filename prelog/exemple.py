from prelog.main import CheckLog
from prelog.main import LEVELS as poglevel
from prelog.main import FORMATS


log = CheckLog(fmt=FORMATS['locate'])


def hello(name):
    log.main.debug(f'Hello {name}')

