"""Tests de la API ergonómica: from_file / from_string / to_*."""

import warnings
from pathlib import Path

import pytest

warnings.filterwarnings("ignore", category=SyntaxWarning)

from netlist2tikz import Schematic


SIMPLE_NETLIST = "R1 1 0; down"
RC_NETLIST = """
V1 1 0_1 ac; down
R1 1 2; right
C1 2 0_2; down
W 0_1 0_2; right
"""


def test_from_string_creates_schematic():
    sch = Schematic.from_string(SIMPLE_NETLIST)
    assert 'R1' in sch.elements


def test_from_string_multiline():
    sch = Schematic.from_string(RC_NETLIST)
    assert {'R1', 'C1', 'V1'}.issubset(set(sch.elements.keys()))


def test_from_file(tmp_path):
    sch_path = tmp_path / 'test.sch'
    sch_path.write_text(SIMPLE_NETLIST + '\n')
    sch = Schematic.from_file(sch_path)
    assert 'R1' in sch.elements


def test_from_file_missing_raises(tmp_path):
    missing = tmp_path / 'no_existe.sch'
    with pytest.raises(FileNotFoundError):
        Schematic.from_file(missing)


def test_to_tikz_standalone_includes_documentclass():
    sch = Schematic.from_string(SIMPLE_NETLIST)
    tikz = sch.to_tikz(standalone=True)
    assert r'\documentclass' in tikz
    assert r'\begin{tikzpicture}' in tikz
    assert r'\end{tikzpicture}' in tikz


def test_to_tikz_fragment_excludes_documentclass():
    sch = Schematic.from_string(SIMPLE_NETLIST)
    tikz = sch.to_tikz(standalone=False)
    assert r'\documentclass' not in tikz
    assert r'\begin{tikzpicture}' in tikz


def test_to_pdf_creates_file(tmp_path):
    sch = Schematic.from_string(SIMPLE_NETLIST)
    out = tmp_path / 'out.pdf'
    sch.to_pdf(out)
    assert out.exists()
    assert out.stat().st_size > 0


def test_to_png_creates_file(tmp_path):
    sch = Schematic.from_string(SIMPLE_NETLIST)
    out = tmp_path / 'out.png'
    sch.to_png(out, dpi=150)
    assert out.exists()
    assert out.stat().st_size > 0


def test_to_pdf_returns_path_string(tmp_path):
    sch = Schematic.from_string(SIMPLE_NETLIST)
    out = tmp_path / 'out.pdf'
    result = sch.to_pdf(out)
    assert result == str(out)


def test_legacy_constructor_still_works(tmp_path):
    """El constructor original con string-netlist sigue funcionando."""
    sch = Schematic(SIMPLE_NETLIST)
    assert 'R1' in sch.elements
    # Y también con path
    sch_path = tmp_path / 'legacy.sch'
    sch_path.write_text(SIMPLE_NETLIST + '\n')
    sch2 = Schematic(str(sch_path))
    assert 'R1' in sch2.elements
