from ast import Attribute, expr
from typing import Callable
from xpytex import expressions

# Attributes Handler
class attributes:
    default: Callable[[str, str], str]
    rules = []

    @classmethod
    def default(cls, parent: str, field: str) -> str:
        return rf'\text{{{parent}}}.\text{{{field}}}'

    @classmethod
    def add_rule(cls, r: Callable[[str, str], str]):
        cls.rules.append(r)

    @classmethod
    def decompress(cls, e: Attribute) -> tuple[expr, str]:
        return (e.value, e.attr)
    
    @classmethod
    def get_rule(cls, t: tuple[str, str]) -> str:
        if len(cls.rules) == 0: return cls.default(*t)

        ys = [f(*t) for f in cls.rules]
        matches = map(lambda x: x != '', ys)
        matches = list(matches)

        if not any(matches):
            # print("Str_Latexifier didn't match any rules, backing to default formatting.")
            return cls.default(*t)
        elif matches.count(True) > 1:
            raise LookupError("Multiple rules match.")
        else:
            return ys[matches.index(True)]

    @classmethod
    def apply(cls, x: Attribute) -> str:
        parent, field = attributes.decompress(x)
        parent = expressions.latexify(parent)
        return cls.get_rule((parent, field))
    
    @classmethod
    def latexify(cls, e: Attribute):
        return cls.apply(e)