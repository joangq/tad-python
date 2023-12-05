from xpytex import expressions
from ast import List

class lists:
    def latexify(ast: List) -> str:
        return '[' + ', '.join(expressions.latexify(x) for x in ast.elts) + ']'