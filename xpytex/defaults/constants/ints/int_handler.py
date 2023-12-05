from typing import List, Callable

class int_handler:
    default: Callable[[int], str]
    rules: List[Callable[[int], str]] = []

    @staticmethod
    def default(x: int) -> str: return str(x)
    
    @classmethod
    def add_rule(cls, rule):
        cls.rules.append(rule)
    
    @classmethod
    def get_rule(cls, x: int) -> Callable[[int], str]:
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
    def apply(cls, x: int) -> str:
        return cls.get_rule(x)