from re import sub

def cast(str_type:str):
    if str_type == 'int':
        return int
    if str_type == 'float':
        return float
    if str_type == 'set':
        return set
    if str_type == 'list': 
        return list
    return str

def is_int(domain:str) -> bool:
    return domain == 'int' or\
        domain.split('(')[0] == 'int'

def is_bool(domain:str) -> bool:
    return domain == 'bool'

def is_matrix(domain:str) -> bool:
    is_there_matrix = domain.split('[')[0].replace(' ','') == "matrixindexedby"
    if not is_there_matrix:
        return False
    return "of" in domain.split(']')[1]

def is_function(domain:str) -> bool:
    is_there_function = "function" == domain.split('(')[0].replace(" ",'')
    if not is_there_function:
        return False
    return '-->' in domain.split('(')[1]

def is_relation(domain:str) -> bool:
    regex = r'(\([a-zA-Z0-9 ]*\))'
    dom = sub(regex, '', domain)
    return dom.split('(')[0].replace(' ', '') == "relationof"

class EssenceType:
    def __init__(self, values:dict, essece_types:str) -> None:
        pass

    def __len__(self) -> int:
        raise NotImplementedError("method __len__ not implemented. It must be implemented by the children class")

    def __hash__(self) -> int:
        raise NotImplementedError("method __hash__ not implemented. It must be implemented by the children class")

    def __str__(self) -> str:
        raise NotImplementedError("method __len__ not implemented. It must be implemented by the children class")

class EssenceMatrix(EssenceType):
    def __init__(self, values:dict, essece_types:str) -> None:
        super().__init__(values, essece_types)
        matrix_types, indexes_types = self.__parse_types(essece_types)
        shape = self.__get_shape(values, indexes_types)
        self.shape = tuple([s[1] for s in shape])
        self.index_types = tuple([s[0] for s in shape])
        self.matrix = self.__create_matrix(values, list(self.index_types), matrix_types)

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

    def __hash__(self) -> int:
        return hash(tuple([tuple(row) for row in self.matrix]))
    
    def __str__(self) -> str:
        return str(self.matrix)       

class EssenceFunction(EssenceType):
    def __init__(self, values: dict, essece_types: str) -> None:
        super().__init__(values, essece_types)
        codomain, domain = self.__parse_types(essece_types)
        self.types = {'domain':domain, 'codomain':codomain}
        self.values = {codomain(k): domain(v) for k,v in values.items()}
        self.domain_values = set(self.values.keys())
        self.codomain_values = set(self.values.values())

    def __parse_types(self, essence_types:str):
        assert "function" in essence_types, 'wrong essence type. Expected function'
        splitted_function = essence_types.split(' --> ')
        codomain = splitted_function[0].split(' ')[-1].split('(')[0]
        domain = splitted_function[1].split('(')[0]
        return cast(codomain), cast(domain)

    def __call__(self, arg):
        return self.values[arg]

    def __len__(self) -> int:
        return len(self.domain_values)

    def __hash__(self) -> int:
        return hash(tuple(list(self.values.items())))

    def __str__(self) -> str:
        return "\n".join([f'{k} -> {v}' for k,v in self.values.items()])

class EssenceRelation(EssenceType):
    def __init__(self, values: list[list], essece_types: str) -> None:
        super().__init__({}, essece_types)
        types = self.__parse_type(essece_types)
        self.values = tuple([tuple([types[i](v[i]) for i in range(len(v))]) for v in values])
        self.relations_len = len(self.values[0])
        self.relation_type = tuple(types)

    def __parse_type(self, essence_type:str) -> list:
        relation_types = essence_type.split("of")[1]
        first_index = relation_types.index("(") + 1
        last_index = [i for i in range(len(relation_types)) if relation_types[i] == ")"][-1]
        inner_types = relation_types[first_index:last_index].split("*")
        inner_types = [cast(t.replace(" ","").split("(")[0]) for t in inner_types]
        return inner_types

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, arg:int|tuple):
        if type(arg) == int:
            return self.values[arg]
        assert isinstance(arg,tuple), f"expected int or tuple, got: {type(arg)}"
        ret_val = self.values[arg[0]]
        for idx in arg[:1]:
            ret_val = ret_val[idx]
        return ret_val

    def __hash__(self) -> int:
        return hash(self.values)

    def __str__(self) -> str:
        return "\n".join([str(v) for v in self.values])

def essence_tuple(tuple_values:list, essence_types:str) -> tuple:
    types = essence_types.split(',')
    types = [cast(t.split('(')[0]) for t in types]
    return tuple([types[i](t) for i,t in enumerate(tuple_values)])

if __name__ == "__main__":   
    EssenceMatrix({'1': {'1': 1, '2': 1, '3': 1, '4': 1, '5': 2, '6': 2, '7': 2, '8': 2}, '2': {'1': 1, '2': 1, '3': 2, '4': 2, '5': 1, '6': 1, '7': 2, '8': 2}, '3': {'1': 1, '2': 2, '3': 1, '4': 2, '5': 1, '6': 2, '7': 1, '8': 2}, '4': {'1': 1, '2': 2, '3': 2, '4': 1, '5': 2, '6': 1, '7': 1, '8': 2}}, "matrix indexed by [int(1..k), int(1..b)] of int(1..g)")

    EssenceFunction({"1": 1, "10": 15, "100": 18, "11": 1, "12": 13, "13": 2, "14": 15, "15": 8, "16": 9, "17": 2, "18": 17, "19": 3,
      "2": 4, "20": 15, "21": 6, "22": 10, "23": 3, "24": 17, "25": 5, "26": 9, "27": 7, "28": 11, "29": 5, "3": 7,
      "30": 17, "31": 1, "32": 10, "33": 8, "34": 15, "35": 5, "36": 12, "37": 5, "38": 10, "39": 7, "4": 15, "40": 11,
      "41": 5, "42": 16, "43": 3, "44": 10, "45": 7, "46": 11, "47": 5, "48": 16, "49": 3, "5": 3, "50": 10, "51": 7,
      "52": 11, "53": 5, "54": 16, "55": 3, "56": 15, "57": 7, "58": 11, "59": 1, "6": 16, "60": 17, "61": 3, "62": 15,
      "63": 7, "64": 9, "65": 5, "66": 17, "67": 5, "68": 11, "69": 6, "7": 2, "70": 15, "71": 5, "72": 17, "73": 7,
      "74": 9, "75": 8, "76": 15, "77": 7, "78": 11, "79": 1, "8": 10, "80": 17, "81": 8, "82": 17, "83": 14, "84": 11,
      "85": 7, "86": 16, "87": 7, "88": 11, "89": 14, "9": 8, "90": 17, "91": 11, "92": 14, "93": 17, "94": 11,
      "95": 14, "96": 17, "97": 11, "98": 14, "99": 17}, "function (total) int(1..n_cars) --> int(1..n_cars)")

    EssenceRelation([[1, 1], [1, 2], [1, 5], [2, 1], [2, 2], [2, 4], [3, 1], [3, 2], [3, 3], [4, 2], [4, 3], [4, 4], [5, 1], [5, 2],
             [6, 1], [6, 5], [7, 1], [7, 4], [8, 1], [8, 3], [9, 2], [9, 5], [10, 2], [10, 4], [11, 2], [11, 3], [12, 3],
             [12, 5], [13, 3], [13, 4], [14, 1], [15, 2], [16, 5], [17, 4], [18, 3]], "relation (minSize 1) of ( int(1..n_classes) * int(1..n_options) )")
