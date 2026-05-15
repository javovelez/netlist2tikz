"""Stub no-op de `state`.

El upstream lcapy gestiona aquí el contexto global de símbolos (sympy) para el
motor de análisis. netlist2tikz solo consume `state.switch_context` y
`state.restore_context` desde `netfile.py` cuando parsea archivos `.sch`
incluidos, y para dibujar esquemáticos no se necesita gestionar contextos
simbólicos.
"""


class _State:
    def switch_context(self, context):
        pass

    def restore_context(self):
        pass


state = _State()
