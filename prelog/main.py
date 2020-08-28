import logging
from colorama import Fore, Back
from contextlib import contextmanager
import wrapt
import inspect
import time

##          Logging Levels              ##
logging.addLevelName(8, "SPC_DBG")
logging.SPC_DBG = logging.DEBUG - 2
logging.addLevelName(12, "CMN_DBG")
logging.CMN_DBG = logging.DEBUG + 2
logging.addLevelName(18, "SPC_INFO")
logging.SPC_INFO = logging.INFO - 2
logging.addLevelName(22, "CMN_INFO")
logging.CMN_INFO = logging.INFO + 2

LEVELS = {"1": logging.SPC_DBG,
          "2": logging.DEBUG,
          "3": logging.CMN_DBG,
          "4": logging.SPC_INFO,
          "5": logging.INFO,
          "6": logging.CMN_INFO}


##          Formats         ##
FORMATS = {
    'classic': ': %(asctime)s:%(levelname)s:%(name)s:%(message)s',
    'light': ': %(message)s',
    'locate': '(%(module)s / %(lineno)d): %(message)s'
}


##          Formatter used in Logger class          ##
class MyFormatter(logging.Formatter):
    def __init__(self, fmt=FORMATS['classic']):
        super().__init__(fmt)

##          Logger used in CheckLog class           ##
class MyLogger(logging.Logger):
    def __init__(self, name, file=False, fmt=FORMATS['classic']):
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
        self.info(Fore.GREEN + message + Fore.RESET)

    def spc_dbg(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.SPC_DBG):
            self._log(logging.SPC_DBG, message, args, **kwargs)

    def cmn_dbg(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.CMN_DBG):
            self._log(logging.CMN_DBG, message, args, **kwargs)

    def spc_info(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.SPC_INFO):
            self._log(logging.SPC_INFO, message, args, **kwargs)

    def cmn_info(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.CMN_INFO):
            self._log(logging.CMN_INFO, message, args, **kwargs)

    def SDS(self, message):
        self.spc_dbg(Back.GREEN + Fore.LIGHTWHITE_EX + message + Back.RESET + Fore.RESET)

    def SDF(self, message):
        self.spc_dbg(Back.RED + Fore.BLACK + message + Back.RESET + Fore.RESET)

    def CDF(self, message):
        self.debug(Back.RED + Fore.BLACK + message + Back.RESET + Fore.RESET)

    def CDS(self, message):
        self.cmn_dbg(Back.GREEN + Fore.LIGHTWHITE_EX + message + Back.RESET + Fore.RESET)

    def SIS(self, message):
        self.spc_dbg(Back.GREEN + Fore.LIGHTWHITE_EX + message + Back.RESET + Fore.RESET)

    def SIF(self, message):
        self.spc_dbg(Back.RED + Fore.BLACK + message + Back.RESET + Fore.RESET)

    def CIF(self, message):
        self.debug(Fore.RED + message + Fore.RESET)

    def CIS(self, message):
        self.cmn_dbg(Fore.GREEN + message + Fore.RESET)


##          Timer decorator to use directly in your code         ##
@wrapt.decorator
def timer(wrapped, instance, args, kwargs):
    a = time.time()
    result = wrapped(*args, **kwargs)
    b = time.time() - a
    return result, b

class CheckLog:
    def __init__(self, fmt=FORMATS['classic']):
        self.LOC = "f'{inspect.getouterframes(inspect.currentframe())[-1][-2]}'"
        self.main = MyLogger(__name__, fmt=Fore.WHITE + 'Main Logger' + fmt + Fore.RESET)
        self.dataIO = MyLogger(__name__, fmt=Fore.MAGENTA + 'Data I/O Logger' + fmt + Fore.RESET)
        self.dataProc = MyLogger(__name__, fmt=Fore.CYAN + 'Data Proc. Logger' + fmt + Fore.RESET)
        self.display = MyLogger(__name__, fmt=Fore.YELLOW + 'Display Logger' + fmt + Fore.RESET)
        self.init = "Init: True"
        self.done = "Completed: True"
        self.error = "Completed: False"
        self.end = "Closed: True"

    ##          Create a new logger that will be used with "self.'id'"          ##
    def create_logger(self, id, color, fmt=FORMATS['classic']):
        setattr(CheckLog, id, MyLogger(__name__, fmt=color + id.upper() + fmt + Fore.RESET))

    ##          A context manager at logging level 'common debug'           ##
    @contextmanager
    def cbugCheck(self, logger, func_name=None):
        func_name = eval(self.LOC) if func_name is None else func_name
        try:
            logger.cmn_dbg(Fore.GREEN + f'{func_name}: {self.init}'+ Fore.RESET)
            yield func_name
            logger.CDS(f'{func_name}: {self.done}')
        except Exception as e:
            logger.CDF(f'{self.error}: {e}')
        finally:
            logger.cmn_dbg(Fore.GREEN + f'{func_name}: {self.end}' + Fore.RESET)

    ##          A context manager at logging level 'specific debug'           ##
    @contextmanager
    def sbugCheck(self, logger, func_name=None):
        func_name = eval(self.LOC) if func_name is None else func_name
        try:
            logger.spc_dbg(Fore.BLUE + f'{func_name}: {self.init}' + Fore.RESET)
            yield
            logger.spc_dbg(Fore.GREEN + f'{func_name}: {self.done}' + Fore.RESET)
        except Exception as e:
            logger.SDF(f'{self.error}: {e}')
        finally:
            logger.spc_dbg(Fore.BLUE + f'{func_name}: {self.end}' + Fore.RESET)

    ##          A timercontext manager          ##
    @contextmanager
    def timeCheck(self, func, *args, **kwargs):
        try:
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            yield result, duration
        except:
            pass
        finally:
            pass



if __name__ == '__main__':

    class Logger(CheckLog):
        def __init__(self):
            super().__init__(fmt=FORMATS['locate'])
            self.main.setLevel((logging.SPC_DBG))
            self.display.setLevel(logging.SPC_DBG)
            self.create_logger('client', Fore.CYAN, fmt=FORMATS['locate'])


    log = Logger()

    def find(x, items):
        with log.sbugCheck(log.dataProc):
            for item in items:
                if item == x:
                    indice = items.index(item)
                    log.dataIO.cmn_dbg(f'{str(item)} = {type(item)}')
            return items.pop(indice)

    items = [n for n in range(0, 5)]
    with log.cbugCheck(log.client):
        for x in range(0, 6):
            result = find(x, items)
    log.main.SDS(f'FINISHED')

    items = [n for n in range(0, 5)]
    for x in range(0, 6):
        find(x, items)
    log.main.SDS(f'FINISHED')

    from prelog.exemple import hello
    hello('world')

    class Finder(CheckLog):
        def __init__(self):
            super().__init__(fmt=FORMATS['locate'])
            self.main.setLevel(logging.SPC_DBG)
            self.display.setLevel(logging.SPC_DBG)

        @timer
        def find(self, x, items):
            with self.sbugCheck(self.main):
                for item in items:
                    if item == x:
                        indice = items.index(item)
                        F.dataIO.cmn_dbg(f'{str(item)} = {type(item)}')
                return items.pop(indice)


    F = Finder()
    # F.main.setLevel(logging.DEBUG)

    def findRange():
        items = [n for n in range(0, 5)]
        with F.cbugCheck(F.main):
            for x in range(0, 6):
                result = F.find(x, items)
                # F.main.spc_dbg(f'{result[1]}')

    result = findRange()

    F.main.SDS(f'{result} FINISHED')

    items = [n for n in range(0, 5)]
    for x in range(0, 6):
        F.find(x, items)
    F.main.SDS(f'FINISHED')

    items = [n for n in range(0, 5)]
    results = []
    for x in range(0, 6):
        with F.timeCheck(F.find, x, items) as result:
            results.append(result)
    F.main.cmn_dbg(f'{[result for result in results]}')

