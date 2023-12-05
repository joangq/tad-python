from xpytex import function_calls

def matrix_constructor_rule(name: str, args: list[str], parent:str|None=None) -> str: 
    if (parent, name) not in [('Matrix', 'of'), ('Matriz','de'), ('numpy', 'array'), ('np', 'array')]: return ''

    prefix = r'\left[\begin{matrix}'
    suffix = r'\end{matrix}\right]'
    if (parent, name) in [('numpy', 'array'), ('np', 'array')]:
        args = args[0][1:-1]
        args = args.split("],")
        args = [[y.strip() for y in x.replace(']', '').replace('[','').split(', ')] for x in args]
        args = [' & '.join(s) for s in args]
        args = r'\\'.join(args)
        return prefix + args + suffix
    
    # Asume que args es una lista de listas latexificadas

    # Assumes the latexified list has elements separated by Literal[", "]
    args = [s.replace(', ', ' ').replace('[', '').replace(']', '').split(' ') for s in args]
    args = [' & '.join(s) for s in args]
    args = r'\\'.join(args)

    return prefix + args + suffix
    
function_calls.add_rule(matrix_constructor_rule)

def matrix_dotproduct_rule(name: str, args: list[str], parent:str|None=None): 
    return r' \cdot{}'.join([parent, *args]) if name in ['productoPunto', 'dotProduct'] else ''
function_calls.add_rule(matrix_dotproduct_rule)

