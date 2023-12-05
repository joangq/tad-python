from ast import Add, Sub, BitAnd, BitOr, BitXor, Mod, Div, FloorDiv, LShift, RShift, Mult, MatMult, Pow
from xpytex import binary_operations


def add_handler(left: str, op, right: str) -> str: return left + '+' + right
def sub_handler(left: str, op, right: str) -> str: return left + '-' + right
def bitAnd_handler(left: str, op, right: str) -> str: return left + r'\texttt{\&}' + right
def bitOr_handler(left: str, op, right: str) -> str: return left + '|' + right
def bitXor_handler(left: str, op, right: str) -> str: return left + r'\oplus{}' + right
def mod_handler(left: str, op, right: str) -> str: return left + r'\texttt{ mod }' + right

def infix_div_handler(left: str, op, right: str) -> str: return left + r'\div{}' + right
def frac_div_handler(left: str, op, right: str) -> str: return rf'\frac{{{left}}}{{{right}}}'

def infix_floorDiv_handler(left: str, op, right: str) -> str: return left + r' \lfloor\div{}\rfloor ' + right
def frac_floorDiv_handler(left: str, op, right: str) -> str: return rf'\left\lfloor\frac{{{left}}}{{{right}}}\right\rfloor'

def lshift_handler(left: str, op, right: str) -> str: return left + r'\texttt{<<}' + right
def rshift_handler(left: str, op, right: str) -> str: return left + r'\texttt{>>}' + right
def mult_handler(left: str, op, right: str) -> str: return left + r'\times{}' + right
def matMult_handler(left: str, op, right: str) -> str: return left + r'{}' + right
def pow_handler(left: str, op, right: str) -> str: return left + r'\hat{}' + right

binary_operations.register_handler(Add, add_handler)
binary_operations.register_handler(Sub, sub_handler)
binary_operations.register_handler(BitAnd, bitAnd_handler)
binary_operations.register_handler(BitOr, bitOr_handler)
binary_operations.register_handler(BitXor, bitXor_handler)
binary_operations.register_handler(Mod, mod_handler)
binary_operations.register_handler(Div, frac_div_handler)
binary_operations.register_handler(FloorDiv, frac_floorDiv_handler)
binary_operations.register_handler(LShift, lshift_handler)
binary_operations.register_handler(RShift, rshift_handler)
binary_operations.register_handler(Mult, mult_handler)
binary_operations.register_handler(MatMult, matMult_handler)
binary_operations.register_handler(Pow, pow_handler);