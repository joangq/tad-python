from xpytex import function_calls

def set_union_rule(name: str, args: list[str], parent:str|None=None):
    return r' \cup{}'.join([parent, *args]) if name == 'union' else ''

def empty_set_rule(name: str, args: list[str], parent:str=None):
    return r'\{\}' if parent == 'Conjunto' and name == 'vacio' else ''

def set_constructor_rule(name: str, args: list[str], parent:str=None):
    return r'\{'+ ', '.join(args) +r'\}' if parent == 'Conjunto' and name == 'de' else ''

def set_intersect_rule(name: str, args: list[str], parent:str|None=None):
    return r' \cap{}'.join([parent, *args]) if name == 'interseccion' else ''

def set_included_rule(name: str, args: list[str], parent:str|None=None):
    return r' \subseteq{}'.join([parent, *args]) if name == 'incluido' else ''


function_calls.add_rule(empty_set_rule)
function_calls.add_rule(set_union_rule)
function_calls.add_rule(set_constructor_rule)
function_calls.add_rule(set_included_rule)
function_calls.add_rule(set_intersect_rule)