from .base import EssenceType
from .helpers import cast

class EssenceTuple(EssenceType):
    """
    Represents an Essence tuple type.

    Args:
        values (list): List of tuple values
        essece_types (str): String representation of tuple types in the Essence language
    """
    def __init__(self, values: list, essece_types: str) -> None:
        """
        Initialize a new EssenceTuple instance.

        Args:
            values (list): List of tuple values
            essece_types (str): String representation of tuple types in the Essence language
        """
        str_types = essece_types.split(',')
        str_types = [t.replace(" ", "").replace("tuple(", "").replace(')','').split('(')[0] for t in str_types]
        self.types = [cast(t.split('(')[0]) for t in str_types]
        self.values = tuple([self.types[i](t) for i,t in enumerate(values)])
        self.__idx = 0
    
    def __len__(self) -> int:
        """
        Get the length of the tuple.

        Returns:
            int: Number of elements in the tuple
        """
        return len(self.values)

    def __hash__(self) -> int:
        """
        Get the hash value of the tuple.

        Returns:
            int: Hash value based on tuple contents
        """
        return hash(self.values)

    def __str__(self) -> str:
        """
        Get string representation of the tuple.

        Returns:
            str: String representation of the tuple
        """
        return str(self.values)

    def __getitem__(self, idx:int):
        """
        Get tuple element by index.

        Args:
            idx (int): Element index

        Returns:
            Any: Tuple element at the specified index
        """
        return self.values[idx]

    def __iter__(self):
        """
        Initialize iteration over tuple elements.

        Returns:
            EssenceTuple: Self instance
        """
        self.__idx = 0
        return self

    def __next__(self):
        """
        Get next element in the iteration.

        Returns:
            Any: Next tuple element

        Raises:
            StopIteration: When no more elements are available
        """
        if self.__idx >= len(self.values):
            raise StopIteration

        val = self.values[self.__idx]
        self.__idx += 1
        return val
