from typing import Dict
from ast import Name

# Names handler
class names:
    # Advantages: It's a 1:1 map of words.
    # Disadvanteges: Doesn't allow for more complicated rules, e.g RegEx
    # (a.k.a. is just for word replacement)
    rules: Dict[str, str] = dict()

    @classmethod
    def default(cls, x: str):
        return str(x)
    
    @classmethod
    def add_rule(cls, k: str, v: str):
        cls.rules[k] = v

    @classmethod
    def decompress(cls, e: Name):
        return e.id
    
    @classmethod
    def latexify(cls, e: Name):
        value = cls.decompress(e)
        return cls.rules.get(value, cls.default(value))