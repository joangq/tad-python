from xpytex import constants
from xpytex.defaults.constants.ints.int_handler import int_handler
from xpytex.defaults.constants.strs.str_handler import str_handler

def str_to_latex(x: str) -> str: return r"\text{``"+x+r"''}"
def bool_to_latex(x: bool) -> str: return r"\texttt{"+str(x)+r"}"
def float_to_latex(x: float) -> str: return str(x)
def complex_to_latex(x: complex) -> str: return str(x).replace('(','').replace(')', '').replace('j',r'\text{j}')

constants.register_handler(str, str_handler.apply)
constants.register_handler(bool, bool_to_latex)
constants.register_handler(int, int_handler.apply)
constants.register_handler(float, float_to_latex)
constants.register_handler(complex, complex_to_latex)