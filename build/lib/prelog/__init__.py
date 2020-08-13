import logging
from colorama import Fore, Back
from contextlib import contextmanager

MAIN_CLASSIC_FORMAT = '%(created)f:%(levelname)s:%(name)s: Main Logger: %(message)s'
DATAIO_CLASSIC_FORMAT = '%(created)f:%(levelname)s:%(name)s: Data I/O Logger: %(message)s'
DATAPROC_CLASSIC_FORMAT = '%(created)f:%(levelname)s:%(name)s: Data Proc. Logger: %(message)s'
DISPLAY_CLASSIC_FORMAT = '%(created)f:%(levelname)s:%(name)s: Display Logger: %(message)s'

class MyFormater(logging.Formatter):
    def __init__(self, fmt = MAIN_CLASSIC_FORMAT):
        super().__init__(fmt)

class MyLogger(logging.Logger):
    def __init__(self, name, file=False, fmt=MAIN_CLASSIC_FORMAT):
        super().__init__(name)
        logging.addLevelName(8, "SPC_DBG")
        logging.SPC_DBG = logging.DEBUG - 2
        logging.addLevelName(12, "CMN_DBG")
        logging.CMN_DBG = logging.DEBUG + 2
        logging.addLevelName(18, "CMN_INFO")
        logging.SPC_INFO = logging.INFO - 2
        logging.addLevelName(22, "SPC_INFO")
        logging.CMN_INFO = logging.INFO + 2
        formatter = MyFormater(fmt)
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

    def SDS(self, message):
        self.spc_dbg(Back.GREEN + message + Back.RESET)

    def SDF(self, message):
        self.spc_dbg(Back.RED + Fore.BLACK + message + Back.RESET + Fore.RESET)

    def CDF(self, message):
        self.debug(Fore.RED + message + Fore.RESET)

    def CDS(self, message):
        self.spc_dbg(Fore.GREEN + message + Fore.RESET)


class CheckLog:
    def __init__(self):
        self.main = MyLogger(__name__, fmt=Fore.WHITE + MAIN_CLASSIC_FORMAT + Fore.RESET)
        self.dataIO = MyLogger(__name__, fmt=Fore.MAGENTA + DATAIO_CLASSIC_FORMAT + Fore.RESET)
        self.dataProc = MyLogger(__name__, fmt=Fore.CYAN + DATAPROC_CLASSIC_FORMAT + Fore.RESET)
        self.display = MyLogger(__name__, fmt=Fore.YELLOW + DISPLAY_CLASSIC_FORMAT + Fore.RESET)
        self.init = "Init"
        self.end = "Done"

    @contextmanager
    def bugCheck(self, logger, func_name, init='Init', end="Completed"):
        try:
            logger.spc_dbg(f'{func_name}: {init}')
            yield
        except Exception as e:
            logger.CDF(e)
        finally:
            logger.log(12, end)
            items.pop()