from typing import NamedTuple, Callable, Dict
from ast import expr, BinOp, Add, Sub, BitAnd, BitOr, BitXor, Mod, Div, FloorDiv, LShift, RShift, Mult, MatMult, Pow
from xpytex import expressions

class BinaryOperation(NamedTuple):
    left: expr
    op: BinOp
    right: expr

    @staticmethod
    def from_AST(e: BinOp):
        return BinaryOperation(e.left, type(e.op), e.right)
    
    def digest(self) -> tuple[str, BinOp, str]:
        return (expressions.latexify(self.left),
                self.op, # TODO: operator here is kinda redudant
                         # but it has the advantage of general
                         # handlers that know the operator.
                expressions.latexify(self.right))
    

# Handler
class binary_operations:
    types: type = Add       \
                | Sub       \
                | BitAnd    \
                | BitOr     \
                | BitXor    \
                | Mod       \
                | Div       \
                | FloorDiv  \
                | LShift    \
                | RShift    \
                | Mult      \
                | MatMult   \
                | Pow 
    
    handlers: Dict['binary_operations.types', Callable[[str, str], str]]
    handlers = dict()

    @classmethod
    def register_handler(cls, k: 'binary_operations.types', h: Callable):
        cls.handlers[k] = h
        return cls

    @classmethod
    def latexify(cls, e: BinOp) -> str:
        binop = binary_operations.decompress(e)
        cls.handlers[binop.op].latexify(binop)
    
    @classmethod
    def decompress(cls, e: BinOp) -> BinaryOperation: 
        return BinaryOperation.from_AST(e)
    
    @classmethod
    def latexify(cls, e: BinOp) -> str:
        binop = binary_operations.decompress(e)
        left, op, right = binop.digest()
        return cls.handlers[op](left, op, right)