from .base import EssenceType
from .helpers import cast

class EssenceTuple(EssenceType):
    def __init__(self, values: list, essece_types: str) -> None:
        str_types = essece_types.split(',')
        str_types = [t.replace(" ", "").replace("tuple(", "").split('(')[0] for t in str_types]
        self.types = [cast(t.split('(')[0]) for t in str_types]
        self.values = tuple([self.types[i](t) for i,t in enumerate(values)])
        self.__idx = 0
    
    def __len__(self) -> int:
        return len(self.values)

    def __hash__(self) -> int:
        return hash(self.values)

    def __str__(self) -> str:
        return str(self.values)

    def __getitem__(self, idx:int):
        return self.values[idx]

    def __iter__(self):
        self.__idx = 0
        return self

    def __next__(self):
        if self.__idx >= len(self.values):
            raise StopIteration

        val = self.values[self.__idx]
        self.__idx += 1
        return val
