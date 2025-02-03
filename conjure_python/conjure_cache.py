import os
from shutil import rmtree

CACHE_DIR = '.cache'

class Cache:
    def __init__(self, cache_dir:str|None=None) -> None:
        self.cache_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), CACHE_DIR)
        if cache_dir is not None:
            self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

    def empty(self):
        rmtree(self.cache_dir, ignore_errors=True)
        os.mkdir(self.cache_dir)

    def create_file(self, file_name:str, file_content:str='') -> bool:
        try:
            with open(os.path.join(self.cache_dir, file_name), 'w') as f:
                f.write(file_content)
                return True
        except:
            return False

    def write(self, file_name:str, file_content:str, create:bool=True) -> bool:
        if not create and not os.path.exists(os.path.join(self.cache_dir, file_name)):
            return False

        return self.create_file(file_name, file_content)

    def append(self, file_name:str, file_content:str) -> bool:
        try:
            with open(os.path.join(self.cache_dir, file_name), 'a') as f:
                f.write(file_content)
                return True
        except:
            return False
