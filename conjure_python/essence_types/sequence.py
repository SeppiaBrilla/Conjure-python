from .base import EssenceType
from .helpers import cast as type_cast

class EssenceSequence(EssenceType):
    def __init__(self, values:list, essece_types:str) -> None:
        set_type_str = essece_types.split("of")[1].replace(" ", '').split('(')[0]
        self.domain_type = type_cast(set_type_str)
        self.values = [self.domain_type(v) for v in values]
        self.__current_idx = 0

    def __len__(self) -> int:
        return len(self.values)

    def __hash__(self) -> int:
        return hash(tuple(self.values))

    def __str__(self) -> str:
        return str(self.values)

    def __iter__(self):
        self.__current_idx = 0
        return self

    def __next__(self):
        if self.__current_idx >= len(self.values):
            raise StopIteration
        val = self.values[self.__current_idx]
        self.__current_idx += 1
        return val

# EssenceSequence([9, 10, 11, 12, 13], "sequence(size 4) of int(3..9)")
