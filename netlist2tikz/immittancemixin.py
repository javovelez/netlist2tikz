"""Stub vacío.

En upstream lcapy `ImmittanceMixin` aporta propiedades de
impedancia/admitancia a la clase `Node` para el análisis simbólico.
netlist2tikz no analiza circuitos: solo necesita la herencia para que la
clase `Node` se construya sin error.
"""


class ImmittanceMixin:
    pass
