from __future__ import annotations
from typing import TypeVar, Generic as Genérico, List as Lista
from tad import TAD, observador, generador, axioma, operacion

T = TypeVar('T')

@TAD
class Secuencia(Genérico[T]):

    # Observadores básicos

    @observador
    def esVacia(s: Secuencia[T]) -> bool: ...

    @observador
    def prim(s: Secuencia[T]) -> T: ...

    @observador
    def fin(s: Secuencia[T]) -> Secuencia[T]: ...

    # Generadores

    @generador
    def vacia() -> Secuencia[T]: ...

    @generador
    def agregarAdelante(s: Secuencia[T], e: T) -> Secuencia[T]: ...

    # Otras Operaciones

    @operacion # xs: N-Tupla[T]
    def de(*xs: T) -> Secuencia[T]: ...

    @operacion
    def agregarAtras(s: Secuencia[T], e: T) -> Secuencia[T]: ...
        
    @operacion
    def concatenar(s: Secuencia[T], t: Secuencia[T]) -> Secuencia[T]: ...

    @operacion
    def ult(s: Secuencia[T]) -> T: ...

    @operacion
    def com(s: Secuencia[T]) -> Secuencia[T]: ...

    @operacion
    def long(s: Secuencia[T]) -> int: ...

    @operacion
    def esta(s: Secuencia[T], e: T) -> bool: ...

    # Axiomas

    @axioma
    def axioma_esVacia(tipo, s: Secuencia[T]) -> bool:
        return tipo.esVacia(s) == (True if s == tipo.vacia() else False)

    @axioma
    def axioma_prim(tipo, s: Secuencia[T], e: T) -> bool:
        return tipo.prim([e, *s]) == e
    
    @axioma
    def axioma_fin(tipo, s: Secuencia[T], e: T) -> bool:
        return tipo.fin([e, *s]) == s

    @axioma
    def axioma_agregarAtras(tipo, s: Secuencia[T], e: T) -> bool:
        return tipo.agregarAtras(s, e) == (tipo.agregarAtras(tipo.vacia(), e) if tipo.esVacia(s) \
                                           else tipo.agregarAdelante(tipo.agregarAtras(tipo.fin(s), e), tipo.prim(s)))
    
    @axioma
    def axioma_concatenar(tipo, s: Secuencia[T], t: T) -> bool:
        return tipo.concatenar(s, t) == (t if tipo.esVacia(s) \
                                         else tipo.agregarAdelante(tipo.concatenar(tipo.fin(s), t), tipo.prim(s)))
    
    @axioma
    def axioma_ult(tipo, s: Secuencia[T]) -> bool:
        return tipo.ult(s) == (tipo.prim(s) if tipo.esVacia(tipo.fin(s)) \
                              else tipo.ult(tipo.fin(s)))

    @axioma
    def axioma_com(tipo, s: Secuencia[T]) -> bool:
        return tipo.com(s) == (tipo.vacia() if tipo.esVacia(tipo.fin(s)) \
                              else tipo.agregarAdelante(tipo.com(tipo.fin(s)), tipo.prim(s)))

    @axioma
    def axioma_long(tipo, s: Secuencia[T]) -> bool:
        return tipo.long(s) == (0 if tipo.esVacia(s) else 1 + tipo.long(tipo.fin(s)))

    @axioma
    def axioma_esta(tipo, s: Secuencia[T], e: T) -> bool:
        return tipo.esta(s, e) == ((not (tipo.esVacia(s))) and \
                                   (e == tipo.prim(s) or tipo.esta(tipo.fin(s), e)))
    

# Implementación
from catthy import EnhancedContainer, DefaultFunctor, NaiveHashable

# Implementación de TAD Secuencia usando una lista funcional (ver módulo 'fun')
class secuencia(Lista[T], NaiveHashable, EnhancedContainer, DefaultFunctor, Secuencia): ...

# Observadores
secuencia.esVacia = lambda s: len(s) == 0
secuencia.fin = lambda s: secuencia(s[1:])
secuencia.prim = lambda s: s[0]

# Generadores
secuencia.vacia = lambda: secuencia()

secuencia.agregarAdelante = lambda s,e: secuencia.de(e, *s)

# Muta s
def secuencia_push(s: secuencia, e: T):
    secuencia.insert(0, e)
    return s
secuencia.push = secuencia_push

# Operaciones
secuencia.de = secuencia.of # Inherited from fun.EnhancedContainer
secuencia.ult = lambda s: s[-1]
secuencia.com = lambda s: s[1:]
secuencia.long = lambda s: len(s)
secuencia.esta = lambda s, e: e in s

secuencia.concatenar = lambda s,t: secuencia.de(*s,*t)

# Muta s
def secuencia_extend(s: secuencia[T], t: secuencia[T]) -> secuencia[T]:
    s.extend(t)
    return s
secuencia.extend = secuencia_extend

secuencia.agregarAtras = lambda s,e: secuencia.de(*s, e)

# Muta s
def secuencia_append(s: secuencia[T], e: T) -> secuencia[T]:
    s.insert(len(s), e)
    return s

secuencia.append = secuencia_append
