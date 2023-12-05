import ast

from xpytex.handlers.expressions import expressions
from xpytex.handlers.constants import constants
from xpytex.handlers.names import names
from xpytex.handlers.attributes import attributes
from xpytex.handlers.comparisons import comparisons
from xpytex.handlers.bool_operations import bool_operations
from xpytex.handlers.binary_operations import binary_operations
from xpytex.handlers.function_calls import function_calls
from xpytex.handlers.lists import lists
from xpytex.handlers.sets import sets
from xpytex.defaults.setup import register_handlers

# TODO: Add support for parsing modules.
# If the module is parsed, then parse it as an algorithm
# using an environment similar to 'algorithmic' in LaTeX
# If not, parse it as an expression. TODO: Add default support for assignment, etc.

# TODO: The automatic behaviour should be:
#   - If the code is multiline, parse it as an algorithm.
#   - If not, parse it as expression.
def latexify(code: str):
    """Try to latexify the code. Currently only latexifies `expressions`."""
    register_handlers(default_handlers=True, default_rules=True)
    AST = ast.parse(code)   # Module AST
    AST = AST.body          # Get the lines of the Module
    AST = AST[0]            # Get the first line
    AST = AST.value         # Get the contents of the line
    return expressions.latexify(AST)