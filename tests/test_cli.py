"""Tests del CLI `n2t`: render y lint, exit codes y formatos."""

import warnings

import pytest

warnings.filterwarnings("ignore", category=SyntaxWarning)

from netlist2tikz.cli import main, EXIT_OK, EXIT_PARSE, EXIT_RENDER, EXIT_IO


SIMPLE = "R1 1 0; down\n"
LOOP = "R1 1 2; right\nW 2 1; right\n"


# ---- lint ------------------------------------------------------------------

def test_lint_ok(tmp_path, capsys):
    p = tmp_path / 'ok.sch'
    p.write_text(SIMPLE)
    rc = main(['lint', str(p)])
    assert rc == EXIT_OK
    captured = capsys.readouterr()
    assert 'OK' in captured.err


def test_lint_missing_file(tmp_path, capsys):
    rc = main(['lint', str(tmp_path / 'no_existe.sch')])
    assert rc == EXIT_IO


# ---- render: formato por extensión ----------------------------------------

def test_render_pdf_inferido_de_extension(tmp_path):
    sch_path = tmp_path / 'r.sch'
    sch_path.write_text(SIMPLE)
    out = tmp_path / 'out.pdf'
    rc = main(['render', str(sch_path), '-o', str(out)])
    assert rc == EXIT_OK
    assert out.exists() and out.stat().st_size > 0


def test_render_png_inferido_de_extension(tmp_path):
    sch_path = tmp_path / 'r.sch'
    sch_path.write_text(SIMPLE)
    out = tmp_path / 'out.png'
    rc = main(['render', str(sch_path), '-o', str(out), '--dpi', '120'])
    assert rc == EXIT_OK
    assert out.exists() and out.stat().st_size > 0


def test_render_tikz_a_stdout(tmp_path, capsys):
    sch_path = tmp_path / 'r.sch'
    sch_path.write_text(SIMPLE)
    rc = main(['render', str(sch_path), '--tikz'])
    assert rc == EXIT_OK
    out = capsys.readouterr().out
    assert r'\documentclass' in out
    assert r'\begin{tikzpicture}' in out


def test_render_tikz_no_standalone(tmp_path, capsys):
    sch_path = tmp_path / 'r.sch'
    sch_path.write_text(SIMPLE)
    rc = main(['render', str(sch_path), '--tikz', '--no-standalone'])
    assert rc == EXIT_OK
    out = capsys.readouterr().out
    assert r'\documentclass' not in out
    assert r'\begin{tikzpicture}' in out


def test_render_flags_no_nodes_no_labels(tmp_path):
    sch_path = tmp_path / 'r.sch'
    sch_path.write_text("V1 1 0_1; down\nR1 1 2 1k; right\nR2 2 0_2 2k; down\nW 0_1 0_2; right\n")
    out = tmp_path / 'pelado.png'
    rc = main(['render', str(sch_path), '-o', str(out),
               '--no-nodes', '--no-labels'])
    assert rc == EXIT_OK
    assert out.exists()


def test_render_missing_input(tmp_path):
    rc = main(['render', str(tmp_path / 'no.sch'), '-o', str(tmp_path / 'out.pdf')])
    assert rc == EXIT_IO


def test_render_loop_topology_fails_with_render_error(tmp_path):
    sch_path = tmp_path / 'loop.sch'
    sch_path.write_text(LOOP)
    out = tmp_path / 'loop.pdf'
    rc = main(['render', str(sch_path), '-o', str(out)])
    assert rc == EXIT_RENDER


def test_render_extension_desconocida_falla(tmp_path):
    sch_path = tmp_path / 'r.sch'
    sch_path.write_text(SIMPLE)
    out = tmp_path / 'out.xyz'
    rc = main(['render', str(sch_path), '-o', str(out)])
    assert rc == EXIT_IO  # no puede inferir formato
