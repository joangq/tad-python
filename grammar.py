from __future__ import annotations
import inspect
from catthy import fun
from typing import Final, Dict, NamedTuple

def parent_module(f: callable) -> str: return f.__qualname__.split('.')[0]

def flatten(s):
    result = []
    for item in s:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

class Parametro(NamedTuple):
    nombre: str
    tipo: str

class Funcion(NamedTuple):
    nombre: str
    parametros: list[Parametro]
    resultado: str
    codigo: list[str]

    @staticmethod
    def from_callable(f: callable) -> Funcion:
        signatura = inspect.signature(f)
        return Funcion(nombre=f.__name__, 
                       resultado=signatura.return_annotation,
                       codigo=inspect.getsourcelines(f),
                       parametros=[Parametro(k,v.annotation if v.kind != inspect._ParameterKind.VAR_POSITIONAL else f"...{v.annotation}") for k,v in \
                                   inspect.signature(f).parameters.items()],
                        )

# Depende de github.com/joangq/tad-latex/tad.sty
class signaturas:
    @classmethod
    def latexify(cls, f: Funcion, symbol: str|None = None) -> str:
        nombre = symbol or '$'+f.nombre+'$' if len(f.nombre) == 1 else rf'\text{{{f.nombre}}}'
        
        resultado = f.resultado
        parametros = [p.tipo for p in f.parametros] + [resultado]

        for i,param in enumerate(parametros):
            p = str(param)
            if '...' in p:
                p = p.replace('...', '')
                p = rf'{p} $\times\dots\times$ {p}'
            parametros[i] = '{'+p+'}'
        
        return ''.join([rf'\signature{{{nombre}}}', *parametros])
        

TRADUCCIONES: Final[Dict[str, str]] = {
    "observers": "observadores",
    "generators": "generadores",
    "operations": "operaciones"
}

def wrap(wrapped: callable):
    """Wraps a function with a wrapper, but preserving some original parameters.
    Works similarly to functools.wrapped, but tries not to replace the signature."""
    def newfunc(wrapper: callable):
        wrapper.__name__ = wrapped.__name__
        wrapper.__qualname__ = wrapped.__qualname__
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__module__ = wrapped.__module__
        wrapper.__annotations__ = wrapped.__annotations__
        return wrapper
    return newfunc
    
# ========================================

def consume_multiple__(n, f, args, acc=None):
    """Helper to consume_multiple"""
    L = ((1 if acc is not None else 0)+len(args))
    if L != n and L%(n-1) != 1: 
        raise Exception(f"Incompatible length {L} for {n} args. Expected {L+1} or {L-1}.")

    if acc is not None:
        offset = 0
    else:
        acc = args[0]
        offset = 1

    n = n-1
    for i in range(offset, len(args)-n+1+offset, n):
        acc = f(acc, *[args[i+j] for j in range(0,n)])
    
    return acc

def consume_multiple(f, args, acc=None):
    """Variadic version of functools.reduce"""
    return consume_multiple__(len(inspect.signature(f).parameters), f, args, acc)

def _multop_to_varadic(multop, parent_module = None):
    if not parent_module:
        parent_module = parent_module(multop)
    
    @wrap(multop)
    def g(name: str, args: list[str], parent: list):
        if name != multop.__name__: return ''
        else:
            if parent == parent_module:
                return consume_multiple(multop, args)
            else:
                return consume_multiple(multop, args, parent)
            
    g.__source__ = inspect.getsource(multop)

    return g

def _unop_to_varadic(unop, parent_module = None):
    """Converts a unary operator to a varadic one to match the latexify Function Call facade."""
    if not parent_module:
        parent_module = parent_module(unop)
    
    @wrap(unop)
    def g(name, args, parent):
        if name != unop.__name__: return ''
        if len(args) > 1:
            raise TypeError("More than one argument in unary operator.")
        
        if len(args) == 0:
            return unop(parent)
        else:
            return unop(args[0])
    
    g.__source__ = inspect.getsource(unop)
    return g

def _binop_to_varadic(binop, parent_module = None):
    """Converts a binary operator to a varadic one to match the latexify Function Call facade."""
    if not parent_module:
        parent_module = parent_module(binop)
    
    @wrap(binop)
    def g(name, args, parent):
        if name != binop.__name__: return ''
        else:
            if parent == parent_module:
                return fun.foldl(binop, args)
            else:
                return fun.foldl(binop, args, parent)
            
    g.__source__ = inspect.getsource(binop)
    return g

def _varop_to_varadic(varop, parent_module = None):
    """Adapts a varadic single-argument operator to the latexify Function call facade"""
    if not parent_module:
        parent_module = parent_module(varop)
    
    @wrap(varop)
    def g(name, args, parent):
        if name != varop.__name__: return ''
        if parent != parent_module: return ''
        return varop(*args)

    g.__source__ = inspect.getsource(varop)
    return g

# ========================================

class Syntax:
    # Assumes that is used on GrammarObjects.
    @staticmethod
    def op_to_variadic(cls: object, converter: callable, op: str) -> callable:
        return converter(getattr(cls, op), getattr(cls, '__tad__'))

    @staticmethod
    def multop_to_varadic(cls, binop: str):
        return _multop_to_varadic(getattr(cls, binop), getattr(cls, '__tad__'))

    @staticmethod
    def unop_to_varadic(cls, unop: str):
        return _unop_to_varadic(getattr(cls, unop), getattr(cls, '__tad__'))
    
    @staticmethod
    def binop_to_varadic(cls, binop: str):
        return _binop_to_varadic(getattr(cls, binop), getattr(cls, '__tad__'))

    @staticmethod
    def varop_to_varadic(cls, varop: str):
        return _varop_to_varadic(getattr(cls, varop), getattr(cls, '__tad__'))
    
    @staticmethod
    def convert_methods(cls):
        for k,v in list(cls.__dict__.items()): # FIXME: Dict changes size on iteration
            if v and isinstance(v, staticmethod):
                rulename = 'rule_'+k
                f = getattr(cls, k)
                ps = inspect.signature(f).parameters
                n = len( ps )
                if n == 2:
                    rule = Syntax.binop_to_varadic(cls, k)
                elif n == 1:
                    if list(ps.items())[0][1].kind is inspect._ParameterKind.VAR_POSITIONAL: # is varadic?
                        rule = Syntax.varop_to_varadic(cls, k)
                    else:
                        rule = Syntax.unop_to_varadic(cls, k)
                elif n == 0:
                    ...
                setattr(cls, rulename, rule)
        return cls


class Grammar(type):
    __tad__: str

    # ADT Functions should be:
    # @staticmethod
    # def f(params... : str) -> str: ...
    @classmethod
    def test(x):
        ...

    def as_latex(self) -> str:
        output = r'\begin{tad}{'+self.__tad__+'}\n'
        for k,v in self.__tadobj__.get_tad().items():
            if k == 'axioms': continue # skip
            output += ('\t'+r'\begin{'+TRADUCCIONES[k]+'}\n')
            for f in v:
                output += ('\t\t'+signaturas.latexify(Funcion.from_callable(f))+'\par\n')
            output += ('\t'+r'\end{'+TRADUCCIONES[k]+'}\n')
        output += (r'\end{tad}\n')
        return output
    
    @classmethod
    def latexify(cls, name: str, args: list[str], parent:None|str=None) -> str:
        return getattr(cls, name)(name, args, parent)

def grammarOf(tad: str):
    def wrapper(cls):
        cls.__tadobj__ = tad
        cls.__tad__ = tad.__name__ # TODO: Use TAD obj
        Syntax.convert_methods(cls)
        return Grammar(cls.__name__, cls.__bases__, dict(cls.__dict__))
    return wrapper