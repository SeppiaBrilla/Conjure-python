from .base import EssenceType
from .helpers import cast

class EssenceMatrix(EssenceType):
    """
    Represents a multi-dimensional matrix in Essence.

    Args:
        values (dict): Dictionary containing matrix values
        essece_types (str): String representation of matrix types in the Essence language
    """
    def __init__(self, values:dict, essece_types:str) -> None:
        """
        Initialize a new EssenceMatrix instance.

        Args:
            values (dict): Dictionary containing matrix values
            essece_types (str): String representation of matrix types in the Essence language
        """
        super().__init__(values, essece_types)
        matrix_types, indexes_types = self.__parse_types(essece_types)
        shape = self.__get_shape(values, indexes_types)
        self.shape = tuple([s[1] for s in shape])
        self.index_types = tuple([s[0] for s in shape])
        self.matrix = self.__create_matrix(values, list(self.index_types), matrix_types)
        self.__current_idx = 0

    def __getitem__(self, idx:int|tuple):
        """
        Get matrix element by index or indices.

        Args:
            idx (int | tuple): Single index or tuple of indices

        Returns:
            Any: Matrix element at the specified position

        Raises:
            AssertionError: If idx is not tuple or hashable type
        """
        if not isinstance(idx, tuple):
            return self.matrix[idx]
        val = self.matrix
        assert isinstance(idx, tuple), f'expecting tuple or ashable type, got: {type(idx)}' 
        for i in idx:
            val = val[i - 1]
        return val

    def __len__(self) -> int:
        """
        Get the length of the first dimension.

        Returns:
            int: Length of the first dimension
        """
        return self.shape[0]

    def __parse_types(self, essence_types:str):
        """
        Parse the matrix type string into matrix and index types.

        Args:
            essence_types (str): String representation of matrix types

        Returns:
            tuple: Tuple of (matrix type, list of index types)

        Raises:
            AssertionError: If input is not a matrix type
        """
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
        """
        Get the shape of the matrix.

        Args:
            values (dict): Matrix values
            types (list[str], optional): List of index types
            current_shape (list, optional): Current shape being built

        Returns:
            list: List of (type, size) tuples representing matrix dimensions
        """
        if current_shape == None:
            current_shape = []
        key = list(values.keys())[0]
        current_shape.append((type(key) if types is None else types[len(current_shape)], len(values.keys())))
        if isinstance(values[key], dict):
            return self.__get_shape(values[key], types=types, current_shape=current_shape)
        return current_shape
    
    def __create_matrix(self, values:dict, types:list, value_type) -> list|dict:
        """
        Create the matrix structure from values.

        Args:
            values (dict): Matrix values
            types (list): List of index types
            value_type: Type of matrix values

        Returns:
            list | dict: Matrix structure
        """
        dict_values = list(values.values())
        if not isinstance(dict_values[0], dict):
            if types[0] == int:
                return [value_type(v) for v in dict_values]
            return {cast(k): value_type(v) for k,v in values.items()}
        if types[0] == int:
            return [self.__create_matrix(v, types[1:], value_type) for v in dict_values]
        return {cast(k): self.__create_matrix(v, types[1:], value_type) for k,v in values.items()}

    def __iter__(self):
        """
        Initialize iteration over matrix elements.

        Returns:
            EssenceMatrix: Self instance
        """
        self.__current_idx = 0
        return self

    def __next__(self):
        """
        Get next element in the iteration.

        Returns:
            Any: Next matrix element

        Raises:
            StopIteration: When no more elements are available
        """
        if self.__current_idx >= len(self):
            raise StopIteration
        el = self.matrix[self.__current_idx]
        self.__current_idx += 1
        return el

    def __hash__(self) -> int:
        """
        Get the hash value of the matrix.

        Returns:
            int: Hash value based on matrix contents
        """
        return hash(tuple([tuple(row) for row in self.matrix]))
    
    def __str__(self) -> str:
        """
        Get string representation of the matrix.

        Returns:
            str: String representation of the matrix
        """
        return str(self.matrix)       
