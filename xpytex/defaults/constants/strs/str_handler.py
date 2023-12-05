from typing import Callable, List

class str_handler:
    default: Callable[[str], str]
    rules: List[Callable[[str], str]] = []

    @staticmethod
    def default(x: str) -> str:
        return r"\text{``"+x+r"''}"
    
    @classmethod
    def add_rule(cls, rule):
        cls.rules.append(rule)
    
    @classmethod
    def get_rule(cls, x: str) -> str:
        if len(cls.rules) == 0: return cls.default(x)

        ys = [f(x) for f in cls.rules]
        matches = map(lambda x: x != '', ys)
        matches = list(matches)

        if not any(matches):
            # print("Str_Latexifier didn't match any rules, backing to default formatting.")
            return cls.default(x)
        elif matches.count(True) > 1:
            raise LookupError("Multiple rules match.")
        else:
            return ys[matches.index(True)]

    @classmethod
    def apply(cls, x: str) -> str:
        return cls.get_rule(x)