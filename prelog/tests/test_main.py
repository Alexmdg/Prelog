import pytest
import unittest
import os, sys, inspect, time
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from main import *


class Test_LoggingLevels(unittest.TestCase):
    log = logging.Logger(__name__)

    def test_addLevels(self):
        errors = []
        if not logging.SPC_DBG:
            errors.append('Special_Debug level not created')
        if not logging.SPC_INFO:
            errors.append('Special_Debug level not created')
        if not logging.CMN_DBG:
            errors.append('Special_Debug level not created')
        if not logging.CMN_INFO:
            errors.append('Special_Debug level not created')
        assert len(errors) == 0

    def test_setLevel_SPC_DBG(self):
        self.log.setLevel(logging.SPC_DBG)
        with self.assertLogs(self.log, level=logging.DEBUG-2) as cm:
            self.log.log(logging.DEBUG-3, 'Test 1')
            self.log.log(logging.DEBUG-2, 'Test 2')
            self.log.log(logging.DEBUG-1, 'Test 3')
            self.log.log(logging.SPC_DBG, 'Test 4')
        self.assertEqual(cm.output, ['SPC_DBG:test_main:Test 2',
                                     'Level 9:test_main:Test 3',
                                     'SPC_DBG:test_main:Test 4'])

    def test_setLevel_SPC_INFO(self):
        self.log.setLevel(logging.SPC_INFO)
        with self.assertLogs(self.log, level=logging.INFO-2) as cm:
            self.log.log(logging.INFO-3, 'Test 1')
            self.log.log(logging.INFO-2, 'Test 2')
            self.log.log(logging.INFO-1, 'Test 3')
            self.log.log(logging.SPC_INFO, 'Test 4')
        self.assertEqual(cm.output, ['SPC_INFO:test_main:Test 2',
                                     'Level 19:test_main:Test 3',
                                     'SPC_INFO:test_main:Test 4'])

    def test_setLevel_CMN_INFO(self):
        self.log.setLevel(logging.CMN_INFO)
        with self.assertLogs(self.log, level=logging.INFO+2) as cm:
            self.log.log(logging.INFO+3, 'Test 1')
            self.log.log(logging.INFO+2, 'Test 2')
            self.log.log(logging.INFO+1, 'Test 3')
            self.log.log(logging.CMN_INFO, 'Test 4')
        self.assertEqual(cm.output, ['Level 23:test_main:Test 1',
                                     'CMN_INFO:test_main:Test 2',
                                     'CMN_INFO:test_main:Test 4'])

    def test_setLevel_CMN_DBG(self):
        self.log.setLevel(logging.CMN_DBG)
        with self.assertLogs(self.log, level=logging.DEBUG+2) as cm:
            self.log.log(logging.DEBUG+3, 'Test 1')
            self.log.log(logging.DEBUG+2, 'Test 2')
            self.log.log(logging.DEBUG+1, 'Test 3')
            self.log.log(logging.CMN_DBG, 'Test 4')
        self.assertEqual(cm.output, ['Level 13:test_main:Test 1',
                                     'CMN_DBG:test_main:Test 2',
                                     'CMN_DBG:test_main:Test 4'])


class Test_MyFormatter(unittest.TestCase):
    log = logging.Logger(__name__ + '2')
    formatter = MyFormatter()
    handler = logging.StreamHandler(formatter)
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    def test_format(self):
        with self.assertLogs(self.log, level=logging.INFO) as cm:
            self.log.info('Test')
        self.assertEqual(cm.output, [f"{time.time()}:INFO:test_main2: Main Logger: Test"])



# class Test_MyLogger:
#     main = MyLogger(__name__)
#
#     def test_MyLogger_init(self):
#         errors = []


class Test_CheckLog:
    log = CheckLog()

    def test_loggerClass_init(self):
        errors = []
        if not self.log.main:
            errors.append('no main logger')
        if not self.log.dataIO:
            errors.append('no dataIO logger')
        if not self.log.dataProc:
            errors.append('no dataProc logger')
        if not self.log.display:
            errors.append('no display logger')
        if self.log.init != 'Init':
            errors.append((f'{self.log.init}: unexpected value for self.init'))
        if self.log.end != 'Completed':
            errors.append((f'{self.log.end}: unexpected value for self.end'))
        assert len(errors) == 0