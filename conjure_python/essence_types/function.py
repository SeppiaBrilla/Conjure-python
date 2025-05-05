from .base import EssenceType
from .helpers import cast

class EssenceFunction(EssenceType):
    def __init__(self, values: dict, essece_types: str) -> None:
        super().__init__(values, essece_types)
        codomain, domain = self.__parse_types(essece_types)
        self.types = {'domain':domain, 'codomain':codomain}
        self.values = {codomain(k): domain(v) for k,v in values.items()}
        self.domain_values = set(self.values.keys())
        self.codomain_values = set(self.values.values())
        self.__current_idx = 0
        self.__items = list(self.values.items())

    def __parse_types(self, essence_types:str):
        assert "function" in essence_types, 'wrong essence type. Expected function'
        splitted_function = essence_types.split(' --> ')
        codomain = splitted_function[0].split(' ')[-1].split('(')[0]
        domain = splitted_function[1].split('(')[0]
        return cast(codomain), cast(domain)

    def __call__(self, arg):
        return self.values[arg]

    def __iter__(self):
        self.__current_idx = 0
        return self

    def __next__(self):
        if self.__current_idx >= len(self):
            raise StopIteration
        el = self.__items[self.__current_idx]
        self.__current_idx += 1
        return el

    def __len__(self) -> int:
        return len(self.domain_values)

    def __hash__(self) -> int:
        return hash(tuple(list(self.values.items())))

    def __str__(self) -> str:
        return "\n".join([f'{k} -> {v}' for k,v in self.values.items()])
