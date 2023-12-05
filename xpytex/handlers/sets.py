from xpytex.handlers.expressions import expressions
from ast import Set

class sets:
    def latexify(ast: Set) -> str:
        return r'\{' + ', '.join(expressions.latexify(x) for x in ast.elts) + r'\}'