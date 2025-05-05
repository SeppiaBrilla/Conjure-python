class EssenceType:
    def __init__(self, values:dict, essece_types:str) -> None:
        pass

    def __len__(self) -> int:
        raise NotImplementedError("method __len__ not implemented. It must be implemented by the children class")

    def __hash__(self) -> int:
        raise NotImplementedError("method __hash__ not implemented. It must be implemented by the children class")

    def __str__(self) -> str:
        raise NotImplementedError("method __len__ not implemented. It must be implemented by the children class")

    def __iter__(self):
        raise NotImplementedError("method __iter__ not implemented. It must be implemented by the children class")

    def __next__(self):
        raise NotImplementedError("method __next__ not implemented. It must be implemented by the children class")


