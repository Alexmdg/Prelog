import logging
from colorama import Fore, Back
from contextlib import contextmanager
import wrapt

MAIN_CLASSIC_FORMAT = '%(created)f:%(levelname)s:%(name)s: Main Logger: %(message)s'
DATAIO_CLASSIC_FORMAT = '%(created)f:%(levelname)s:%(name)s: Data I/O Logger: %(message)s'
DATAPROC_CLASSIC_FORMAT = '%(created)f:%(levelname)s:%(name)s: Data Proc. Logger: %(message)s'
DISPLAY_CLASSIC_FORMAT = '%(created)f:%(levelname)s:%(name)s: Display Logger: %(message)s'

MAIN_LIGHT_FORMAT = '%(name)s: Main Logger: %(message)s'
DATAIO_LIGHT_FORMAT = '%(name)s: Data I/O Logger: %(message)s'
DATAPROC_LIGHT_FORMAT = '%(name)s: Data Proc. Logger: %(message)s'
DISPLAY_LIGHT_FORMAT = '%(name)s: Display Logger: %(message)s'

logging.addLevelName(8, "SPC_DBG")
logging.SPC_DBG = logging.DEBUG - 2
logging.addLevelName(12, "CMN_DBG")
logging.CMN_DBG = logging.DEBUG + 2
logging.addLevelName(18, "SPC_INFO")
logging.SPC_INFO = logging.INFO - 2
logging.addLevelName(22, "CMN_INFO")
logging.CMN_INFO = logging.INFO + 2

class MyFormatter(logging.Formatter):
    def __init__(self, fmt=MAIN_CLASSIC_FORMAT):
        super().__init__(fmt)

class MyLogger(logging.Logger):
    def __init__(self, name, file=False, fmt=MAIN_CLASSIC_FORMAT):
        super().__init__(name)
        formatter = MyFormatter(fmt)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.addHandler(handler)
        if file is True :
            filelogger = logging.getLogger(f"f_{name}")
            filehandler = logging.FileHandler(f"{name}.log")
            filehandler.setFormatter(formatter)
            filelogger.addHandler(filehandler)

    def success(self, message):
        self.info(Fore.GREEN + message)

    def spc_dbg(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.SPC_DBG):
            self._log(logging.SPC_DBG, message, args, **kwargs)

    def cmn_dbg(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.CMN_DBG):
            self._log(logging.CMN_DBG, message, args, **kwargs)


    def SDS(self, message):
        self.spc_dbg(Back.GREEN + Fore.LIGHTWHITE_EX + message + Back.RESET + Fore.RESET)

    def SDF(self, message):
        self.spc_dbg(Back.RED + Fore.BLACK + message + Back.RESET + Fore.RESET)

    def CDF(self, message):
        self.debug(Fore.RED + message + Fore.RESET)

    def CDS(self, message):
        self.cmn_dbg(Fore.GREEN + message + Fore.RESET)

@wrapt.decorator
def empty_logs(wrapped, instance, args, kwargs):
    init = "Init: True" if not 'init' in kwargs else kwargs['init']
    done = "Completed: True" if not 'done' in kwargs else kwargs['done']
    error = "Completed: False" if not 'error' in kwargs else kwargs['error']
    end = "Closed: True" if not 'end' in kwargs else kwargs['end']
    return wrapped(*args, **kwargs, init=init, done=done, error=error, end=end)

class CheckLog:
    def __init__(self):
        self.main = MyLogger(__name__, fmt=Fore.WHITE + MAIN_CLASSIC_FORMAT + Fore.RESET)
        self.dataIO = MyLogger(__name__, fmt=Fore.MAGENTA + DATAIO_CLASSIC_FORMAT + Fore.RESET)
        self.dataProc = MyLogger(__name__, fmt=Fore.CYAN + DATAPROC_CLASSIC_FORMAT + Fore.RESET)
        self.display = MyLogger(__name__, fmt=Fore.YELLOW + DISPLAY_CLASSIC_FORMAT + Fore.RESET)
        self.init = "Init: True"
        self.done = "Completed: True"
        self.error = "Completed: False"
        self.end = "Closed: True"

    def create_logger(self, name, color, format=MAIN_CLASSIC_FORMAT):
        setattr(CheckLog, name, MyLogger(__name__, fmt=color + format + Fore.RESET))

    @contextmanager
    @empty_logs
    def bugCheck(self, logger, func_name="Current Function", init=None, done=None, error=None, end=None):
        try:
            logger.CDS(f'{func_name}: {init}')
            yield
            logger.CDS(f'{func_name}: {done}')
        except Exception as e:
            logger.CDF(f'{error}: {e}')
        finally:
            logger.CDS(f'{func_name}: {end}')

    # @contextmanager
    # @empty_logs
    # def resultCheck(self, logger, func, init=None, done=None, error=None, end=None):
    #     try:
    #         logger.cmn_dbg(f'{init}')
    #         yield func
    #         logger.cmn_dbg(f'{done}')
    #     except Exception as e:
    #         logger.exception(f'{error}: {e}')
    #     finally:
    #         logger.cmn_dbg(f'{end}')


if __name__ == '__main__':
    log = CheckLog()
    log.main.setLevel(logging.SPC_DBG)
    log.display.setLevel(logging.SPC_DBG)

    def find(x, items):
        for item in items:
            if item == x:
                indice = items.index(item)
        return items.pop(indice)


    items = [n for n in range(0, 5)]
    with log.bugCheck(log.main, 'find(x, items)'):
        for x in range(0, 6):
            result = find(x, items)
            log.dataIO.cmn_dbg(f'{str(result)} = {type(result)}')

    log.main.SDS(f'FINISHED')

    items = [n for n in range(0, 5)]
    for x in range(0, 6):
        with log.bugCheck(log.main, 'find(x, items)'):
            result = find(x, items)
            log.dataIO.cmn_dbg(f'{str(result)} = {type(result)}')

    log.main.SDS(f'FINISHED')

    # items = [n for n in range(0, 5)]
    # for x in range(0, 6):
    #     with log.resultCheck(log.main, find(x, items)) as result:
    #         log.dataIO.cmn_dbg(f'{str(result)} = {type(result)}')
    #
    # log.main.SDS(f'FINISHED')

    items = [n for n in range(0, 5)]
    for x in range(0, 5):
        result = find(x, items)
        log.main.success(f'{str(result)} = {type(result)}')

    log.main.SDS(f'FINISHED')

    items = [n for n in range(0, 5)]
    for x in range(0, 5):
        log.main.success(f'{str(find(x, items))} = {type(find(x, items))}')