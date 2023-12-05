from ast import And, Or, BoolOp
from typing import Callable
from xpytex import expressions

# Boolean Operations handler (And/Or)
class bool_operations:
    types: type = And | Or

    handlers = dict()

    @classmethod
    def register_handler(cls, k: 'bool_operations.types', h: Callable):
        cls.handlers[k] = h
        return cls

    @classmethod
    def latexify(cls, e: BoolOp) -> str:
        binop = bool_operations.decompress(e)
        cls.handlers[binop.op].latexify(binop)
    
    @classmethod
    def decompress(cls, e: BoolOp) -> tuple: 
        return (type(e.op), [expressions.latexify(x) for x in e.values])
    
    @classmethod
    def latexify(cls, e: BoolOp) -> str:
        op, values = bool_operations.decompress(e)
        return cls.handlers[op](values)