from typing import Callable, Dict
from ast import expr, Constant

# Constants handler
class constants:
    types: type = str | bytes | bool | int | float | complex # None | Ellipsis
    d: Callable[[expr], object] # Expr -> Decompressed

    handlers: Dict['constants.types', Callable[[object], str]]
    handlers = dict()

    def __init__(self, *args, **kwargs):
        raise TypeError("Cannot create 'constants' instances.")

    @classmethod
    def decompress(cls, e: Constant) -> 'constants.types': return e.value

    @classmethod
    def register_handler(cls, k: 'constants.types', h: Callable):
        cls.handlers[k] = h
        return cls

    @classmethod
    def latexify(cls, e: Constant) -> str:
        value = cls.decompress(e)
        return cls.handlers[type(value)](value)