from .base import EssenceType
from .helpers import cast as type_cast

class EssenceSequence(EssenceType):
    """
    Represents an Essence sequence type.

    Args:
        values (list): List of sequence values
        essece_types (str): String representation of sequence types in the Essence language
    """
    def __init__(self, values:list, essece_types:str) -> None:
        """
        Initialize a new EssenceSequence instance.

        Args:
            values (list): List of sequence values
            essece_types (str): String representation of sequence type in the Essence language
        """
        set_type_str = essece_types.split("of")[1].replace(" ", '').split('(')[0]
        self.domain_type = type_cast(set_type_str)
        self.values = [self.domain_type(v) for v in values]
        self.__current_idx = 0

    def __len__(self) -> int:
        """
        Get the length of the sequence.

        Returns:
            int: Number of elements in the sequence
        """
        return len(self.values)

    def __getitem__(self, idx:int):
        """
        Get sequence element by index.

        Args:
            idx (int): Element index

        Returns:
            Any: Sequence element at the specified index
        """
        return self.values[idx]

    def __hash__(self) -> int:
        """
        Get the hash value of the sequence.

        Returns:
            int: Hash value based on sequence contents
        """
        return hash(tuple(self.values))

    def __str__(self) -> str:
        """
        Get string representation of the sequence.

        Returns:
            str: String representation of the sequence
        """
        return str(self.values)

    def __iter__(self):
        """
        Initialize iteration over sequence elements.

        Returns:
            EssenceSequence: Self instance
        """
        self.__current_idx = 0
        return self

    def __next__(self):
        """
        Get next element in the iteration.

        Returns:
            Any: Next sequence element

        Raises:
            StopIteration: When no more elements are available
        """
        if self.__current_idx >= len(self.values):
            raise StopIteration
        val = self.values[self.__current_idx]
        self.__current_idx += 1
        return val

# EssenceSequence([9, 10, 11, 12, 13], "sequence(size 4) of int(3..9)")
