"""Stub vacío.

En el upstream lcapy este módulo define la clase `Expr`, wrapper sobre
sympy con el motor simbólico de circuitos. netlist2tikz trabaja con
sympy directamente: el stub solo existe para que los
`isinstance(expr, Expr)` que viven dentro de `printing.py` no exploten
en ImportError.
"""


class Expr:
    pass
