"""Smoke tests: importar el paquete y parsear un netlist sin requerir LaTeX."""

from netlist2tikz import Schematic


NETLIST_RLC = """
P1 1 0.1; down
R1 3 1; right
L1 2 3; right
C1 3 0; down
P2 2 0.2; down
W 0 0.1; right
W 0.2 0.2; right
"""


def test_import_schematic():
    assert Schematic is not None


def test_parse_rlc():
    sch = Schematic(NETLIST_RLC)
    assert len(sch.elements) > 0
    names = set(sch.elements.keys())
    assert {'R1', 'L1', 'C1', 'P1', 'P2'}.issubset(names)


def test_parse_simple_divider():
    sch = Schematic("R1 1 2 1; right\nR2 2 0 2; down\nW 1 0; left=2")
    assert 'R1' in sch.elements
    assert 'R2' in sch.elements
