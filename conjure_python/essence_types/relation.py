from .base import EssenceType
from .helpers import cast

class EssenceRelation(EssenceType):
    """
    Represents an Essence relation type.

    Args:
        values (list[list]): List of relation values
        essece_types (str): String representation of relation types in the Essence language
    """
    def __init__(self, values: list[list], essece_types: str) -> None:
        """
        Initialize a new EssenceRelation instance.

        Args:
            values (list[list]): List of relation values
            essece_types (str): String representation of relation types in the Essence language
        """
        super().__init__({}, essece_types)
        types = self.__parse_type(essece_types)
        self.values = tuple([tuple([types[i](v[i]) for i in range(len(v))]) for v in values])
        self.relations_len = len(self.values[0])
        self.relation_type = tuple(types)
        self.__current_idx = 0

    def __parse_type(self, essence_type:str) -> list:
        """
        Parse the relation type string into component types.

        Args:
            essence_type (str): String representation of relation type

        Returns:
            list: List of component types
        """
        relation_types = essence_type.split("of")[1]
        first_index = relation_types.index("(") + 1
        last_index = [i for i in range(len(relation_types)) if relation_types[i] == ")"][-1]
        inner_types = relation_types[first_index:last_index].split("*")
        inner_types = [cast(t.replace(" ","").split("(")[0]) for t in inner_types]
        return inner_types

    def __len__(self) -> int:
        """
        Get the number of relations.

        Returns:
            int: Number of relations
        """
        return len(self.values)

    def __getitem__(self, arg:int|tuple):
        """
        Get relation element by index or nested indices.

        Args:
            arg (int | tuple): Single index or tuple of indices

        Returns:
            tuple | Any: Relation element or nested element

        Raises:
            AssertionError: If arg is not int or tuple
        """
        if type(arg) == int:
            return self.values[arg]
        assert isinstance(arg,tuple), f"expected int or tuple, got: {type(arg)}"
        ret_val = self.values[arg[0]]
        for idx in arg[1:]:
            ret_val = ret_val[idx]
        return ret_val

    def __iter__(self):
        """
        Initialize iteration over relation elements.

        Returns:
            EssenceRelation: Self instance
        """
        self.__current_idx = 0
        return self

    def __next__(self):
        """
        Get next element in the iteration.

        Returns:
            tuple: Next relation element

        Raises:
            StopIteration: When no more elements are available
        """
        if self.__current_idx >= len(self):
            raise StopIteration
        el = self.values[self.__current_idx]
        self.__current_idx += 1
        return el

    def __hash__(self) -> int:
        """
        Get the hash value of the relation.

        Returns:
            int: Hash value based on relation contents
        """
        return hash(self.values)

    def __str__(self) -> str:
        """
        Get string representation of the relation.

        Returns:
            str: Formatted string of relation elements
        """
        return "\n".join([str(v) for v in self.values])
