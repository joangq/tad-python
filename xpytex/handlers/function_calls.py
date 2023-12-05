from typing import NamedTuple, Callable, List
from ast import expr, Call, Attribute
from xpytex import expressions

# Type Representation
class FunctionCall(NamedTuple):
    name: expr
    args: list[expr]
    parent: None | expr

    @staticmethod
    def from_AST(e: Call):
        func = e.func
        return FunctionCall(func.attr, e.args, func.value) if type(func) == Attribute \
               else FunctionCall(func, e.args, None)

    def latexify(self):
            return (self.name if type(self.name) == str else expressions.latexify(self.name), 
                    [expressions.latexify(x) for x in self.args], 
                    expressions.latexify(self.parent) if self.parent else None)
    
# Handler
class function_calls:
    default: Callable[[tuple[str, list[str], None|str]], str]
    rules: List[Callable[[str, list[str], None|str], str]] = []

    @staticmethod
    def default(name: str, args: list[str], parent:str|None=None) -> str:
        return (rf'\text{{{parent}}}.' if parent else '') + rf"{name}({', '.join(args)})"

    @classmethod
    def add_rule(cls, rule):
        cls.rules.append(rule)

    @classmethod
    def get_rule(cls, f: FunctionCall) -> str:
        if len(cls.rules) == 0: return cls.default(*f)

        gs = [r(*f) for r in cls.rules]
        matches = map(lambda x: x != '', gs)
        matches = list(matches)

        if not any(matches):
            # print("Str_Latexifier didn't match any rules, backing to default formatting.")
            return cls.default(*f)
        elif matches.count(True) > 1:
            raise LookupError("Multiple rules match.")
        else:
            return gs[matches.index(True)]

    @classmethod
    def decompress(cls, e: Call) -> FunctionCall:
        return FunctionCall.from_AST(e)
    
    @classmethod
    def latexify(cls, e: Call) -> str:
        f = cls.decompress(e)
        f = f.latexify()
        f = tuple(f)
        return cls.get_rule(f)