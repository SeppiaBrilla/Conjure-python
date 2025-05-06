from .base import EssenceType
from typing import cast
from .helpers import cast as type_cast
from collections.abc import Hashable
# find S: set (size 5) of int(9..16)
# {"S": [9, 10, 11, 12, 13]}

class EssenceSet(EssenceType):
    """
    Represents an Essence set type.

    Args:
        values (list): List of set values
        essece_types (str): String representation of set types in the Essence language
    """
    def __init__(self, values:list, essece_types:str) -> None:
        """
        Initialize a new EssenceSet instance.

        Args:
            values (list): List of set values
            essece_types (str): String representation of set types in the Essence language
        """
        set_type_str = essece_types.split("of")[1].replace(" ", '').split('(')[0]
        self.domain_type = type_cast(set_type_str)
        self.__list_values = [cast(Hashable, self.domain_type(v)) for v in values]
        self.values = set(self.__list_values) 
        self.__current_idx = 0

    def __len__(self) -> int:
        """
        Get the number of elements in the set.

        Returns:
            int: Number of elements in the set
        """
        return len(self.values)

    def __hash__(self) -> int:
        """
        Get the hash value of the set.

        Returns:
            int: Hash value based on set contents
        """
        return hash(tuple(self.values))

    def __str__(self) -> str:
        """
        Get string representation of the set.

        Returns:
            str: String representation of the set
        """
        return str(self.values)

    def __iter__(self):
        """
        Initialize iteration over set elements.

        Returns:
            EssenceSet: Self instance
        """
        self.__current_idx = 0
        return self

    def __next__(self):
        """
        Get next element in the iteration.

        Returns:
            Any: Next set element

        Raises:
            StopIteration: When no more elements are available
        """
        if self.__current_idx >= len(self.__list_values):
            raise StopIteration
        val = self.__list_values[self.__current_idx]
        self.__current_idx += 1
        return val

# EssenceSet([9, 10, 11, 12, 13], "find S: set (size 5) of int(9..16)")
