# TAD • Python

Ésta biblioteca es una utilidad para trabajar con TADs (Tipos Abstractos de Datos) en Python. La idea es poder crear clases primero de manera abstracta, especificando qué funciones son observadores, generadores u otras operaciones; junto con
una serie de axiomas para la corroboración de correctitud. Usando los decoradores, luego se puede crear automáticamente código en LaTeX para visualizar el TAD correctamente. Adicionalmente, se podría hacer un uso inteligente de
los axiomas para testear la implementación del TAD.

> [!NOTE]
> El código de LaTeX depende fuertemente de
> [tad-latex](https://www.github.com/joangq/tad-latex)

> [!IMPORTANT]
> Este proyecto está aún sin terminar. Si bien el prototipo funciona
> relativamente bien, todavía está acoplado a ésta implementación de `xpytex`.
> En el futuro, la idea es usar `xpytex` como biblioteca externa.

# Uso

> [!NOTE]
> Ejemplo completo en [secuencia.py](./secuencia.py)

## Clase Abstracta

Primero, definimos la clase como un TAD y la escribimos de forma abstracta, sin dar su implementación.

```python
@TAD
class Secuencia(Genérico[T]):
  @observador
  def esVacia(s: Secuencia[T]) -> bool: ...

  @generador
  def vacia() -> Secuencia[T]: ...

  @generador
  def agregarAdelante(s: Secuencia[T], e: T) -> Secuencia[T]: ...

  @operacion # xs: N-Tupla[T]
  def de(*xs: T) -> Secuencia[T]: ...

  @operacion
  def agregarAtras(s: Secuencia[T], e: T) -> Secuencia[T]: ...

  @axioma
  def axioma_agregarAtras(tipo, s: Secuencia[T], e: T) -> bool:
    return tipo.agregarAtras(s, e) == (tipo.agregarAtras(tipo.vacia(), e) if tipo.esVacia(s) \
            else tipo.agregarAdelante(tipo.agregarAtras(tipo.fin(s), e), tipo.prim(s)))
```

Luego, es necesario definir la gramática del TAD. (Véase [secuencias.ipynb](./secuencias.ipynb))

```python
@grammarOf(Secuencia)
class secuencias:
    """Grammar for a sequence"""
    @staticmethod
    def esVacia(s): return r'\text{vacía?}('+s+')'

    @staticmethod
    def vacia(): return r'\langle\rangle'

    @staticmethod
    def agregarAdelante(s, e): return e+r'\text{ }\bullet{}\text{ }'+s

    @staticmethod
    def de(*xs): return r'\left\langle{}'+ ', '.join(xs) +r'\right\rangle{}'

    @staticmethod
    def agregarAdelante(s, e): return e+r'\text{ }\bullet{}\text{ }'+s
```

Por último, queda exportar la gramática a LaTeX:

```python
secuencias.as_latex()
```
```latex
\begin{tad}{Secuencia}
    \begin{observadores}
    	\signature{\text{esVacia}}{Secuencia[T]}{bool}\par
    	\signature{\text{prim}}{Secuencia[T]}{T}\par
    	\signature{\text{fin}}{Secuencia[T]}{Secuencia[T]}\par
    \end{observadores}
    \begin{generadores}
    	\signature{\text{vacia}}{Secuencia[T]}\par
    	\signature{\text{agregarAdelante}}{Secuencia[T]}{T}{Secuencia[T]}\par
    \end{generadores}
    \begin{operaciones}
    	\signature{\text{ult}}{Secuencia[T]}{T}\par
    	\signature{\text{de}}{T $\times\dots\times$ T}{Secuencia[T]}\par
    	\signature{\text{long}}{Secuencia[T]}{int}\par
    	\signature{\text{concatenar}}{Secuencia[T]}{Secuencia[T]}{Secuencia[T]}\par
    	\signature{\text{com}}{Secuencia[T]}{Secuencia[T]}\par
    	\signature{\text{agregarAtras}}{Secuencia[T]}{T}{Secuencia[T]}\par
    	\signature{\text{esta}}{Secuencia[T]}{T}{bool}\par
    \end{operaciones}
\end{tad}\n
```

## Testeo con Axiomas

Luego de tener nuestro TAD, podemos implementar la clase.

```python
from catthy import NaiveHashable, FactoryConstructor, DefaultFunctor
from typing import List as Lista

# Implementación de Secuencia
class secuencia(Lista[T], NaiveHashable, EnhancedContainer, DefaultFunctor, Secuencia): 
  ...

secuencia.vacia = lambda: secuencia()
secuencia.esVacia = lambda s: len(s) == 0
secuencia.de = secuencia.of # Heredado de catthy.FactoryConstructor
secuencia.agregarAdelante = lambda s,e: secuencia.de(e, *s)
secuencia.agregarAtras = lambda s,e: secuencia.de(*s, e)
```

Luego, podemos testear con los axiomas, por ejemplo, a través de:

```python
agregarAtras_tests = [([], 3),([1,2], 3),([x for x in range(10_000)], 12_345),]

agregarAtras_test_results = [secuencia.axioma_agregarAtras(*x) for x in agregarAtras_tests]
print(all(agregarAtras_test_results))
``` 

(Ver ejemplo completo en [secuencia-tests.ipynb](./secuencia-tests.ipynb))
