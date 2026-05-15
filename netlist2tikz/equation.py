"""Stub vacío.

En el upstream lcapy este módulo define la clase `Equation` para ecuaciones
simbólicas. netlist2tikz no las usa: el stub solo existe para que los
`isinstance(expr, Equation)` que viven dentro de `printing.py` no exploten
en ImportError. Como ningún objeto del paquete instancia esta clase, los
isinstance siempre fallan y el flujo cae al printer estándar de sympy.
"""


class Equation:
    pass
