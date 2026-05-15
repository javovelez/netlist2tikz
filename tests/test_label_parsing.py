"""Tests de regresión para el bug de labels con comas internas (BUG_LABELS_COMMA.md).

El parser de opciones cortaba en cualquier `,` ignorando contextos LaTeX,
con lo cual labels con `\\,` (espacio fino) o coma decimal `{,}` quedaban
truncadas y producían PDFs vacíos sin error.
"""

import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning)

from netlist2tikz import Schematic
from netlist2tikz.opts import Opts


# ---- nivel unitario: split de opts -----------------------------------------

def test_split_respeta_backslash_coma():
    """`\\,` no debe romper el split (caso típico: 5\\,I_1)."""
    opts = Opts("down, l=5\\,I_1, color=blue")
    assert opts['l'] == '5\\,I_1'
    assert opts['color'] == 'blue'
    assert 'down' in opts


def test_split_respeta_backslash_punto_y_coma():
    """`\\;` (espacio medio) tampoco debe romper."""
    opts = Opts("right, l=A\\;B")
    assert opts['l'] == 'A\\;B'


def test_split_respeta_coma_decimal_en_llaves():
    """`{,}` (coma decimal española) ya funcionaba, no debe regresionar."""
    opts = Opts("down, l=16{,}2\\,V_a")
    assert opts['l'] == '16{,}2\\,V_a'


def test_split_combinacion_llaves_y_backslash():
    opts = Opts("down, l={r_m\\,I_1}, color=red")
    assert opts['l'] == '{r_m\\,I_1}'
    assert opts['color'] == 'red'


# ---- nivel integración: render preserva la label --------------------------

def _tikz_of(line):
    sch = Schematic.from_string(line + "\n")
    return sch.to_tikz(standalone=False)


def test_label_thinspace_aparece_en_tikz():
    tikz = _tikz_of("V1 1 0; down, l=5\\,I_1")
    assert '5\\,I_1' in tikz, tikz


def test_label_coma_decimal_aparece_en_tikz():
    tikz = _tikz_of("R1 1 0; down, l=16{,}2\\,V")
    assert '16{,}2' in tikz
    assert '\\,V' in tikz


def test_casos_reales_tp_cuadripolos():
    """Labels equivalentes a los casos del TP3 de TCII (BUG_LABELS_COMMA.md
    tabla). Usamos V/R como portadores genéricos del label porque F y H
    requieren un Vcontrol adicional en la sintaxis."""
    casos = [
        ("V1 1 0; down, l=6\\,I_2",       '6\\,I_2'),
        ("V1 1 0; down, l=5\\,I_1",       '5\\,I_1'),
        ("V1 1 0; down, l=16{,}2\\,V_a",  '16{,}2\\,V_a'),
        ("V1 1 0; down, l=r_m\\,I_1",     'r_m\\,I_1'),
        ("V1 1 0; down, l=0{,}0395\\,V_1", '0{,}0395\\,V_1'),
    ]
    for line, expected in casos:
        tikz = _tikz_of(line)
        assert expected in tikz, f"Falta {expected!r} en netlist {line!r}: {tikz}"
