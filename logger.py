import abc
from enum import Enum
from typing import Literal
from sys import stdout, stderr
from datetime import datetime

class Verbosity(Enum):
    Debug = 0
    Info = 1
    Warning = 2
    Error = 3

    def __lt__(self, other):
        if isinstance(other, Verbosity):
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Verbosity):
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Verbosity):
            return self.value > other.value
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Verbosity):
            return self.value >= other.value
        return NotImplemented

class Logger(metaclass=abc.ABCMeta):
    def __init__(self, verbosity_level:Verbosity) -> None:
        self.verbosity_level = verbosity_level

    @abc.abstractmethod
    def Warn(self, msg:str):
        pass
    @abc.abstractmethod
    def Error(self, msg:str, exception:Exception|None=None):
        pass
    @abc.abstractmethod
    def Info(self, msg:str):
        pass
    @abc.abstractmethod
    def Debug(self, msg:str):
        pass

class Printlogger(Logger):
    def __init__(self, verbosity_level: Verbosity, print_file:Literal['stdout','stderr']='stdout') -> None:
        super().__init__(verbosity_level)
        self.file = stdout if print_file == 'stdout' else stderr

    def __print(self, msg:str) -> None:
        print(msg, file=self.file)

    def Warn(self, msg: str):
        if self.verbosity_level <= Verbosity.Warning:
            self.__print(f'[WARN - {datetime.now()}] {msg}')

    def Error(self, msg: str, exception:Exception|None=None):
        if exception is not None:
            msg = f'{msg} ({exception})'
        if self.verbosity_level == Verbosity.Error:
            self.__print(f'[ERROR - {datetime.now()}] {msg}')

    def Info(self, msg: str):
        if self.verbosity_level <= Verbosity.Info:
            self.__print(f'[INFO - {datetime.now()}] {msg}')

    def Debug(self, msg: str):
        if self.verbosity_level == Verbosity.Debug:
            self.__print(f'[DEBUG - {datetime.now()}] {msg}')
