import os
from logger import Logger

CACHE_DIR = '.cache'

class Cache:
    def __init__(self, cache_dir:str|None=None, logger:Logger|None=None) -> None:
        self.cache_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), CACHE_DIR)
        self.logger = logger
        if cache_dir is not None:
            if self.logger is not None:
                self.logger.Debug(f'cache dir updated to: {cache_dir}')
            self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

    def empty(self):
        if not self.logger is None:
            self.logger.Info(f'emptying cache dir: {self.cache_dir}')
        try:
            os.remove(self.cache_dir)
            os.mkdir(self.cache_dir)
        except Exception as e:
            if not self.logger is None:
                self.logger.Error(f'cannot empty cache dir: {self.cache_dir}', e)

    def create_file(self, file_name:str, file_content:str='') -> bool:
        try:
            with open(os.path.join(self.cache_dir, file_name), 'w') as f:
                f.write(file_content)
                if self.logger is not None:
                    self.logger.Info(f'file {file_name} created under {self.cache_dir} and written.')
                return True
        except Exception as e:
            if self.logger is not None:
                self.logger.Error(f'file {file_name} cannot be created under {self.cache_dir} and written.', e)
            return False

    def write(self, file_name:str, file_content:str, create:bool=True) -> bool:
        if not create and not os.path.exists(os.path.join(self.cache_dir, file_name)):
            if self.logger is not None:
                self.logger.Warn(f'trying to write on a non-existing file: {file_name} with the create flag set to False')

        return self.create_file(file_name, file_content)

    def append(self, file_name:str, file_content:str) -> bool:
        try:
            with open(os.path.join(self.cache_dir, file_name), 'a') as f:
                f.write(file_content)
                if self.logger is not None:
                    self.logger.Info(f'appent to file {file_name} under {self.cache_dir}.')
                return True
        except Exception as e:
            if self.logger is not None:
                self.logger.Error(f'cannot append to file {file_name}', e)
            return False
