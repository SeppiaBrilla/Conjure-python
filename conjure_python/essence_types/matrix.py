from .base import EssenceType
from .helpers import cast

class EssenceMatrix(EssenceType):
    def __init__(self, values:dict, essece_types:str) -> None:
        super().__init__(values, essece_types)
        matrix_types, indexes_types = self.__parse_types(essece_types)
        shape = self.__get_shape(values, indexes_types)
        self.shape = tuple([s[1] for s in shape])
        self.index_types = tuple([s[0] for s in shape])
        self.matrix = self.__create_matrix(values, list(self.index_types), matrix_types)
        self.__current_idx = 0

    def __getitem__(self, idx:int|tuple):
        if not isinstance(idx, tuple):
            return self.matrix[idx]
        val = self.matrix
        assert isinstance(idx, tuple), f'expecting tuple or ashable type, got: {type(idx)}' 
        for i in idx:
            val = val[i]
        return val

    def __len__(self) -> int:
        return self.shape[0]

    def __parse_types(self, essence_types:str):
        assert "matrix" in essence_types, 'wrong essence type. Expected matrix'
        matrix_type = cast(essence_types.split(" of ")[1].split('(')[0].replace(" ", ""))
        open_b = essence_types.index("[")
        close_b = essence_types.index("]")
        indexes_str = essence_types[open_b+1:close_b]
        indexes = []
        for index in indexes_str.split(','):
            indexes.append(cast(index.split('(')[0].replace(" ", "")))
        return matrix_type, indexes

    def __get_shape(self, values:dict, types:list[str]|None=None, current_shape:list|None=None) -> list:
        if current_shape == None:
            current_shape = []
        key = list(values.keys())[0]
        current_shape.append((type(key) if types is None else types[len(current_shape)], len(values.keys())))
        if isinstance(values[key], dict):
            return self.__get_shape(values[key], types=types, current_shape=current_shape)
        return current_shape
    
    def __create_matrix(self, values:dict, types:list, value_type) -> list|dict:
        dict_values = list(values.values())
        if not isinstance(dict_values[0], dict):
            if types[0] == int:
                return [value_type(v) for v in dict_values]
            return {cast(k): value_type(v) for k,v in values.items()}
        if types[0] == int:
            return [self.__create_matrix(v, types[1:], value_type) for v in dict_values]
        return {cast(k): self.__create_matrix(v, types[1:], value_type) for k,v in values.items()}

    def __iter__(self):
        self.__current_idx = 0
        return self

    def __next__(self):
        if self.__current_idx >= len(self):
            raise StopIteration
        el = self.matrix[self.__current_idx]
        self.__current_idx += 1
        return el

    def __hash__(self) -> int:
        return hash(tuple([tuple(row) for row in self.matrix]))
    
    def __str__(self) -> str:
        return str(self.matrix)       
