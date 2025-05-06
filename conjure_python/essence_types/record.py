from .base import EssenceType
from .helpers import is_int, is_bool

class EssenceRecord(EssenceType):
    """
    Represents an Essence record type.

    Args:
        values (dict): Dictionary of record values
        essece_types (str): String representation of record types in the Essence language
    """
    def __init__(self, values:dict, essece_types:str) -> None:
        """
        Initialize a new EssenceRecord instance.

        Args:
            values (dict): Dictionary of record values
            essece_types (str): String representation of record types in the Essence language
        """
        record_keys = list(values.keys())
        self.record_types = self.__get_types(essece_types, record_keys)
        self.__values = {k: self.record_types[k](v) for k,v in values.items()}
        self.__keys = list(self.__values.keys())
        self.__current_key_idx = 0

    def __get_types(self, essence_types:str, essence_keys:list[str]) -> dict:
        """
        Parse record types from the essence type string.

        Args:
            essence_types (str): String representation of record types in the Essence language
            essence_keys (list[str]): List of available record keys

        Returns:
            dict: Dictionary mapping keys to their types

        Raises:
            AssertionError: If a key in the type string is not found in available keys
        """
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
        """
        Get the keys of the record.

        Returns:
            list: List of record keys
        """
        return self.__values.keys()

    def items(self):
        """
        Get the items of the record as key-value pairs.

        Returns:
            list: List of (key, value) pairs
        """
        return self.__values.items()

    def values(self):
        """
        Get the values of the record.

        Returns:
            list: List of record values
        """
        return self.__values.values()

    def __len__(self) -> int:
        """
        Get the number of fields in the record.

        Returns:
            int: Number of fields
        """
        return len(self.__values)

    def __getitem__(self, arg:str):
        """
        Get record value by key.

        Args:
            arg (str): Key to access

        Returns:
            Any: Value associated with the key
        """
        return self.__values[arg]

    def __iter__(self):
        """
        Initialize iteration over record values.

        Returns:
            EssenceRecord: Self instance
        """
        self.__current_key_idx = 0
        return self

    def __next__(self):
        """
        Get next value in the iteration.

        Returns:
            Any: Next record value

        Raises:
            StopIteration: When no more values are available
        """
        if self.__current_key_idx >= len(self):
            raise StopIteration
        el = self.__values[self.__keys[self.__current_key_idx]]
        self.__current_key_idx += 1
        return el

    def __hash__(self) -> int:
        """
        Get the hash value of the record.

        Returns:
            int: Hash value based on record items
        """
        return hash(tuple([itm for itm in self.__values.items()]))

    def __str__(self) -> str:
        """
        Get string representation of the record.

        Returns:
            str: Formatted string of record fields
        """
        return "\n".join([f'{k}: {v}' for k, v in self.__values.items()])
