def __class_of_method(f: callable) -> str:
    return f.__qualname__.split('.')[0]

class tad(type):
    _template = {'observers': set(), 'generators': set(), 'operations': set(), 'axioms': set()}
    __tads__ = dict()

    @classmethod
    @property
    def template(cls): return tad._template.copy()

    def __new__(meta, name, bases, dct):
        dct['get_tad'] = classmethod(lambda cls: tad.__tads__[name])

        # Create the class using the original metaclass
        return super(tad, meta).__new__(meta, name, bases, dct)
    
    @classmethod
    def set_property(cls, tadname: str, property: str, value: object):
        tad.__tads__.setdefault(tadname, tad.template)[property].add(value)
    
def observador(f: callable):
    tad.set_property(__class_of_method(f), 'observers', f)
    return staticmethod(lambda cls, *args: f(*args))

def generador(f: callable):
    tad.set_property(__class_of_method(f), 'generators', f)
    return staticmethod(lambda cls, *args: f(*args))

def operacion(f: callable):
    tad.set_property(__class_of_method(f), 'operations', f)
    return staticmethod(lambda cls, *args: f(*args))

def axioma(f: callable):
    tad.set_property(__class_of_method(f), 'axioms', f)
    return classmethod(lambda cls, *args: f(cls, *args))

# A decorator for the 'tad' metaclass.
# It serves as syntactic sugar, but also it's necessary for initializing
# the 'tad' registry dictionary.
def TAD(cls):
    tad.__tads__.setdefault(cls.__name__, tad.template)
    # Create a new class with the specified metaclass
    return tad(cls.__name__, cls.__bases__, dict(cls.__dict__))
