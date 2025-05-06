from .base import EssenceType
from .helpers import cast

class EssenceFunction(EssenceType):
    """
    Represents a function mapping between two Essence types.

    Args:
        values (dict): Dictionary of function values
        essece_types (str): String representation of function types in the Essence language
    """
    def __init__(self, values:dict, essece_types:str) -> None:
        """
        Initialize a new EssenceFunction instance.

        Args:
            values (dict): Dictionary of function values
            essece_types (str): String representation of function types in the Essence language
        """
        super().__init__(values, essece_types)
        codomain, domain = self.__parse_types(essece_types)
        self.types = {'domain':domain, 'codomain':codomain}
        self.values = {codomain(k): domain(v) for k,v in values.items()}
        self.domain_values = set(self.values.keys())
        self.codomain_values = set(self.values.values())
        self.__current_idx = 0
        self.__items = list(self.values.items())

    def __parse_types(self, essence_types:str):
        """
        Parse the function type string into domain and codomain types.

        Args:
            essence_types (str): String representation of function types

        Returns:
            tuple: Tuple of (codomain type, domain type)

        Raises:
            AssertionError: If input is not a function type
        """
        assert "function" in essence_types, 'wrong essence type. Expected function'
        splitted_function = essence_types.split(' --> ')
        codomain = splitted_function[0].split(' ')[-1].split('(')[0]
        domain = splitted_function[1].split('(')[0]
        return cast(codomain), cast(domain)

    def __call__(self, arg):
        """
        Call the function with an argument.

        Args:
            arg: Function argument

        Returns:
            Any: Function value for the given argument
        """
        return self.values[arg]

    def __iter__(self):
        """
        Initialize iteration over function items.

        Returns:
            EssenceFunction: Self instance
        """
        self.__current_idx = 0
        return self

    def __next__(self):
        """
        Get next item in the iteration.

        Returns:
            tuple: Next (key, value) pair

        Raises:
            StopIteration: When no more items are available
        """
        if self.__current_idx >= len(self):
            raise StopIteration
        el = self.__items[self.__current_idx]
        self.__current_idx += 1
        return el

    def __len__(self) -> int:
        """
        Get the number of elements in the domain.

        Returns:
            int: Number of elements in the domain
        """
        return len(self.domain_values)

    def __hash__(self) -> int:
        """
        Get the hash value of the function.

        Returns:
            int: Hash value based on function items
        """
        return hash(tuple(list(self.values.items())))

    def __str__(self) -> str:
        """
        Get string representation of the function.

        Returns:
            str: Formatted string of function mappings
        """
        return "\n".join([f'{k} -> {v}' for k,v in self.values.items()])
