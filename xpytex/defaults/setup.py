from ast import Constant, Name, Attribute, Compare, BoolOp, BinOp, Call, List, Set

from xpytex import expressions
from xpytex import constants
from xpytex import names
from xpytex import attributes
from xpytex import comparisons
from xpytex import bool_operations
from xpytex import binary_operations
from xpytex import function_calls
from xpytex import lists
from xpytex import sets

def use_default_handlers():
    # print('Using default handlers.')
    from .constants import (int_handler, 
                            str_handler, 
                            other_handlers) # registers int and str handlers

    #from .comparisons import *

    from .binops import binops_handlers
    from .booleans import bool_handlers

def use_default_rules():
    # print('Using default rules.')
    #from .constants.ints.rules import demo_rules
    from .constants.strs.rules import demo_rules
    from .names import names_rules
    from .attrs import attrs_rules
    from .functions import matrix_rules, sequence_rules, set_rules


def register_handlers(default_handlers=False, default_rules=False):
    # print('Initializing xpytex...')
    if default_handlers: use_default_handlers()
    if default_rules: use_default_rules()

    expressions.register_handler(Constant, constants)
    expressions.register_handler(Name, names)
    expressions.register_handler(Attribute, attributes)
    expressions.register_handler(Compare, comparisons)
    expressions.register_handler(BoolOp, bool_operations)
    expressions.register_handler(BinOp, binary_operations)
    expressions.register_handler(Call, function_calls)
    expressions.register_handler(List, lists)
    expressions.register_handler(Set, sets)