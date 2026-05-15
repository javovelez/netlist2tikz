"""netlist2tikz: convierte netlists tipo SPICE en código circuitikz/TikZ.

Fork extractivo de lcapy (https://github.com/mph-/lcapy) — solo el subsistema
de dibujo de esquemáticos, sin el motor de análisis simbólico.
"""

from .schematic import Schematic

__all__ = ['Schematic']
__version__ = '0.1.0'
