from .base import EssenceType
from .helpers import is_int, is_bool

class EssenceRecord(EssenceType):
    def __init__(self, values: dict, essece_types: str) -> None:
        record_keys = list(values.keys())
        self.record_types = self.__get_types(essece_types, record_keys)
        self.__values = {k: self.record_types[k](v) for k,v in values.items()}
        self.__keys = list(self.__values.keys())
        self.__current_key_idx = 0

    def __get_types(self, essence_types:str, essence_keys:list[str]) -> dict:
        essence_types = essence_types.split('{')[1].replace('}','')
        types = {}
        for element in essence_types.split(','):
            element_split = element.split(':')
            key, element_type = element_split[0].replace(' ',''), element_split[1].replace(' ','')
            assert key in essence_keys, f"cannot find key {key}. available keys are: {essence_keys}"
            if is_int(element_type):
                types[key] = int
            elif is_bool(element_type):
                types[key] = bool
            else:
                types[key] = str
        return types

    def keys(self):
        return self.__values.keys()

    def items(self):
        return self.__values.items()

    def values(self):
        return self.__values.values()

    def __len__(self) -> int:
        return len(self.__values)

    def __getitem__(self, arg:str):
        return self.__values[arg]

    def __iter__(self):
        self.__current_key_idx = 0
        return self

    def __next__(self):
        if self.__current_key_idx >= len(self):
            raise StopIteration
        el = self.__values[self.__keys[self.__current_key_idx]]
        self.__current_key_idx += 1
        return el

    def __hash__(self) -> int:
        return hash(tuple([itm for itm in self.__values.items()]))

    def __str__(self) -> str:
        return "\n".join([f'{k}: {v}' for k, v in self.__values.items()])


