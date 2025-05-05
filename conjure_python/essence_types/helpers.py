from re import sub

def cast(str_type:str):
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
    return domain == 'int' or\
        domain.split('(')[0] == 'int'

def is_bool(domain:str) -> bool:
    return domain == 'bool'

def is_matrix(domain:str) -> bool:
    is_there_matrix = domain.split('[')[0].replace(' ','') == "matrixindexedby"
    if not is_there_matrix:
        return False
    return "of" in domain.split(']')[1]

def is_function(domain:str) -> bool:
    is_there_function = "function" == domain.split('(')[0].replace(" ",'')
    if not is_there_function:
        return False
    return '-->' in domain.split('(')[1]

def is_relation(domain:str) -> bool:
    regex = r'(\([a-zA-Z0-9 ]*\))'
    dom = sub(regex, '', domain)
    return dom.split('(')[0].replace(' ', '') == "relationof"

def is_record(domain:str) -> bool:
    return "record" in domain and "{" in domain and "}" in domain

def is_tuple(domain:str) -> bool:
    return domain[0] == "(" and domain[-1] == ")"


