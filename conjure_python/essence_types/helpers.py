from re import sub

def cast(str_type:str):
    """
    Convert string type to Python type.

    Args:
        str_type (str):string representation of type

    Returns:
        type: Corresponding Python type
    """
    if str_type == 'int':
        return int
    if str_type == 'float':
        return float
    if str_type == 'set':
        return set
    if str_type == 'list': 
        return list
    if str_type == 'bool':
        return bool
    return str

def is_int(domain:str) -> bool:
    """
    Check if domain represents an integer type.

    Args:
        domain (str): Domain string

    Returns:
        bool: True if domain is an integer type, False otherwise
    """
    return domain == 'int' or\
        domain.split('(')[0] == 'int'

def is_bool(domain:str) -> bool:
    """
    Check if domain represents a boolean type.

    Args:
        domain (str): Domain string

    Returns:
        bool: True if domain is a boolean type, False otherwise
    """
    return domain == 'bool'

def is_matrix(domain:str) -> bool:
    """
    Check if domain represents a matrix type.

    Args:
        domain (str): Domain string

    Returns:
        bool: True if domain is a matrix type, False otherwise
    """
    is_there_matrix = domain.split('[')[0].replace(' ','') == "matrixindexedby"
    if not is_there_matrix:
        return False
    return "of" in domain.split(']')[1]

def is_function(domain:str) -> bool:
    """
    Check if domain represents a function type.

    Args:
        domain (str): Domain string

    Returns:
        bool: True if domain is a function type, False otherwise
    """
    is_there_function = "function" == domain.split('(')[0].replace(" ",'')
    if not is_there_function:
        return False
    return '-->' in domain.split('(')[1]

def is_relation(domain:str) -> bool:
    """
    Check if domain represents a relation type.

    Args:
        domain (str): Domain string

    Returns:
        bool: True if domain is a relation type, False otherwise
    """
    regex = r'(\([a-zA-Z0-9 ]*\))'
    dom = sub(regex, '', domain)
    return dom.split('(')[0].replace(' ', '') == "relationof"

def is_record(domain:str) -> bool:
    """
    Check if domain represents a record type.

    Args:
        domain (str): Domain string

    Returns:
        bool: True if domain is a record type, False otherwise
    """
    return "record" in domain and "{" in domain and "}" in domain

def is_tuple(domain:str) -> bool:
    """
    Check if domain represents a tuple type.

    Args:
        domain (str): Domain string

    Returns:
        bool: True if domain is a tuple type, False otherwise
    """
    return domain[0] == "(" and domain[-1] == ")"

def is_set(domain:str) -> bool:
    """
    Check if domain represents a set type.

    Args:
        domain (str): Domain string

    Returns:
        bool: True if domain is a set type, False otherwise
    """
    return (domain[0] == '{' and domain[1] == '}') or ('set' in domain and 'mset' not in domain)

def is_sequence(domain:str) -> bool:
    """
    Check if domain represents a sequence type.

    Args:
        domain (str): Domain string

    Returns:
        bool: True if domain is a sequence type, False otherwise
    """
    return 'sequence' in domain
