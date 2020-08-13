import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

from prelog.main import *


class Test_MyLogger:
    log = MyLogger()

    def test_loggerClass_init(self):
        errors = []
        if not log.main