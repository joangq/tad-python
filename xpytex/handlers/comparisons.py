from ast import Eq, Gt, GtE, In, Is, IsNot, Lt, LtE, NotEq, NotIn, Compare
from typing import Callable
from xpytex import expressions

# Comparisons handler
class comparisons:
    types: type = Eq    \
                | Gt    \
                | GtE   \
                | In    \
                | Is    \
                | IsNot \
                | Lt    \
                | LtE   \
                | NotEq \
                | NotIn
    
    symbols = {
        Eq:r'{=}_{\text{obs}}',
        Gt:r'{>}',
        GtE:r'\geqslant{}',
        In:r'\in{}',
        Is:r'\equiv{}',
        IsNot:r'\not\equiv{}',
        Lt:r'{<}',
        LtE:r'\leqslant{}',
        NotEq:r'{\neq}_{\text{obs}}',
        NotIn:r'\notin{}'
    }

    # handlers: Dict['comparisons.types', Callable[[str, ast.Compare, str], str]]
    # handlers = dict()
    f: Callable[[list[str], list['comparisons.types']], str]
    

    @classmethod
    def f(cls, operands: list[str], operators: list['comparisons.types']) -> str:
        return ' '.join(f'{x} {y}' for x,y in zip(operands, [comparisons.symbols[z] for z in operators])) + \
                        (operands[-1] if len(operands) > len(operators) else '')

    @classmethod
    def define_handler(cls, f: Callable[[list[str], list['comparisons.types']], str]): cls.f = f

    @classmethod
    def decompress(cls, e: Compare): return ([expressions.latexify(x) for x in [e.left, *e.comparators]], 
                                                  [type(x) for x in e.ops])

    @classmethod
    def latexify(cls, e: Compare) -> str:
        return comparisons.f(*comparisons.decompress(e))