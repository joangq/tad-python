from xpytex import function_calls

# TODO: Maybe encapsulate this into a "sequence_handler"
# to include scattered code from other handlers.

def seq_constructor_rule(name: str, args: list[str], parent:str=None) -> str: 
    return r'\left\langle{}'+ ', '.join(args) +r'\right\rangle{}' if parent == 'Secuencia' and name == 'de' else ''


def seq_append_rule(name: str, args: list[str], parent:str|None=None) -> str: 
    if name != 'agregarAdelante': return ''
    print(name, args, parent)
    if parent.lower() == 'secuencia':
        ...
        #parent = args.pop(0)
    newargs = [*reversed(args), parent]
    return r' \bullet{}'.join(newargs)


def seq_push_rule(name: str, args: list[str], parent:str|None=None) -> str: 
    newargs = args if parent.lower() == 'secuencia' else [parent, *args]
    return r' \circ{}'.join(newargs) if name == 'agregarAtras' else ''


def seq_concat_rule(name: str, args: list[str], parent:str|None=None) -> str: 
    return r' \texttt{ \& }'.   join([parent, *args]) if name == 'concatenar' else ''


def seq_isempty_rule(name: str, args: list[str], parent:str|None=None) -> str: 
    return r'\text{vacía}?(' + parent + ')' if name == 'esVacia' else ''


def seq_is_in_rule(name: str, args: list[str], parent:str|None=None) -> str: 
    return r'\text{está}?(' + args[0] + ', ' + parent + ')' if name == 'esta' else ''

function_calls.add_rule(seq_constructor_rule)
function_calls.add_rule(seq_append_rule)
function_calls.add_rule(seq_push_rule)
function_calls.add_rule(seq_concat_rule)
function_calls.add_rule(seq_isempty_rule)
function_calls.add_rule(seq_is_in_rule)