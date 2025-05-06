class EssenceType:
    """
    Base class for all Essence types.

    Args:
        values (dict): Dictionary containing values
        essece_types (str): String representation of Essence types
    """
    def __init__(self, values:dict, essece_types:str) -> None:
        """
        Initialize the EssenceType instance.

        Args:
            values (dict): Dictionary containing values
            essece_types (str): String representation of Essence types
        """
        pass

    def __len__(self) -> int:
        """
        Get the length of the Essence type.

        Raises:
            NotImplementedError: Must be implemented by child classes
        """
        raise NotImplementedError("method __len__ not implemented. It must be implemented by the children class")

    def __hash__(self) -> int:
        """
        Get the hash value of the Essence type.

        Raises:
            NotImplementedError: Must be implemented by child classes
        """
        raise NotImplementedError("method __hash__ not implemented. It must be implemented by the children class")

    def __str__(self) -> str:
        """
        Get string representation of the Essence type.

        Raises:
            NotImplementedError: Must be implemented by child classes
        """
        raise NotImplementedError("method __str__ not implemented. It must be implemented by the children class")

    def __iter__(self):
        """
        Get iterator for the Essence type.

        Raises:
            NotImplementedError: Must be implemented by child classes
        """
        raise NotImplementedError("method __iter__ not implemented. It must be implemented by the children class")

    def __next__(self):
        """
        Get next item in the iteration.

        Raises:
            NotImplementedError: Must be implemented by child classes
        """
        raise NotImplementedError("method __next__ not implemented. It must be implemented by the children class")
