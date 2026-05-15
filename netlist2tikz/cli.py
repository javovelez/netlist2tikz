"""CLI `n2t` para netlist2tikz.

Uso resumido (`n2t --help` para detalles):

    n2t render circuito.sch -o circuito.pdf
    n2t render circuito.sch --png -o circuito.png --dpi 600
    n2t render circuito.sch --tikz             # imprime TikZ a stdout
    n2t lint circuito.sch                      # exit 0 si parsea, 1 si no

Códigos de salida:
    0  OK
    1  netlist inválido (error de parseo)
    2  error de render (LaTeX o placer)
    3  error de I/O (archivo no existe, permisos, etc.)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__

EXIT_OK = 0
EXIT_PARSE = 1
EXIT_RENDER = 2
EXIT_IO = 3

_EXT_TO_FORMAT = {
    '.pdf': 'pdf',
    '.png': 'png',
    '.svg': 'svg',
    '.tex': 'tikz',
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='n2t',
        description='Genera esquemáticos circuitikz a partir de netlists.',
    )
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s {__version__}')
    sub = parser.add_subparsers(dest='cmd', required=True)

    # render -----------------------------------------------------------------
    p_render = sub.add_parser(
        'render',
        help='Renderiza un netlist a PDF/PNG/SVG/TikZ.',
    )
    p_render.add_argument('input', type=Path, help='Archivo .sch a renderizar.')
    p_render.add_argument('-o', '--output', type=Path,
                          help='Archivo de salida. Si se omite y se usa '
                               '--tikz, escribe a stdout; en otro caso usa '
                               'el mismo nombre del input con la extensión '
                               'inferida.')
    fmt = p_render.add_mutually_exclusive_group()
    fmt.add_argument('--pdf', action='store_const', const='pdf',
                     dest='format', help='Fuerza salida PDF.')
    fmt.add_argument('--png', action='store_const', const='png',
                     dest='format', help='Fuerza salida PNG.')
    fmt.add_argument('--svg', action='store_const', const='svg',
                     dest='format', help='Fuerza salida SVG.')
    fmt.add_argument('--tikz', action='store_const', const='tikz',
                     dest='format', help='Imprime código TikZ standalone.')
    p_render.add_argument('--no-standalone', action='store_true',
                          help='Con --tikz, emite solo el bloque '
                               '\\begin{tikzpicture}...\\end{tikzpicture} '
                               '(para \\input{} en otro documento).')
    p_render.add_argument('--dpi', type=int, default=300,
                          help='Resolución del PNG (default 300).')
    p_render.add_argument('--style',
                          choices=['american', 'british', 'european'],
                          help='Estilo de símbolos R/L (default american).')
    p_render.add_argument('--no-nodes', action='store_true',
                          help='No dibuja puntos en los nodos.')
    p_render.add_argument('--no-labels', action='store_true',
                          help='No muestra nombres ni valores.')
    p_render.add_argument('--scale', type=float,
                          help='Escala global del esquemático.')

    # lint -------------------------------------------------------------------
    p_lint = sub.add_parser(
        'lint',
        help='Valida que un netlist se parsea sin errores.',
    )
    p_lint.add_argument('input', type=Path, help='Archivo .sch a validar.')

    return parser


def _resolve_format(args) -> str:
    """Devuelve uno de 'pdf'/'png'/'svg'/'tikz' según flags + extensión."""
    if args.format:
        return args.format
    if args.output:
        suffix = args.output.suffix.lower()
        if suffix in _EXT_TO_FORMAT:
            return _EXT_TO_FORMAT[suffix]
        raise ValueError(
            f"No puedo inferir formato desde la extensión {suffix!r}. "
            "Usá --pdf/--png/--svg/--tikz o un -o con extensión conocida."
        )
    # Sin format ni output: default a PDF
    return 'pdf'


def _resolve_output(args, fmt: str) -> Path | None:
    """Devuelve la ruta de salida o None si va a stdout."""
    if args.output:
        return args.output
    if fmt == 'tikz':
        return None  # stdout
    return args.input.with_suffix('.' + fmt)


def _draw_opts(args) -> dict:
    """Traduce flags del CLI a kwargs de Schematic.draw()."""
    opts = {}
    if args.style:
        opts['style'] = args.style
    if args.scale:
        opts['scale'] = args.scale
    if args.no_nodes:
        opts['draw_nodes'] = 'none'
        opts['label_nodes'] = 'none'
    if args.no_labels:
        opts['label_ids'] = False
        opts['label_values'] = False
    return opts


def _cmd_render(args) -> int:
    from .schematic import Schematic

    if not args.input.exists():
        print(f'n2t: error: archivo no encontrado: {args.input}',
              file=sys.stderr)
        return EXIT_IO

    try:
        sch = Schematic.from_file(args.input)
    except Exception as exc:
        print(f'n2t: error de parseo en {args.input}: {exc}',
              file=sys.stderr)
        return EXIT_PARSE

    try:
        fmt = _resolve_format(args)
    except ValueError as exc:
        print(f'n2t: {exc}', file=sys.stderr)
        return EXIT_IO

    opts = _draw_opts(args)
    out = _resolve_output(args, fmt)

    try:
        if fmt == 'tikz':
            content = sch.to_tikz(
                standalone=not args.no_standalone, **opts)
            if out is None:
                sys.stdout.write(content)
            else:
                out.write_text(content)
                print(f'Escrito: {out}', file=sys.stderr)
        elif fmt == 'pdf':
            sch.to_pdf(out, **opts)
            print(f'Escrito: {out}', file=sys.stderr)
        elif fmt == 'png':
            sch.to_png(out, dpi=args.dpi, **opts)
            print(f'Escrito: {out}', file=sys.stderr)
        elif fmt == 'svg':
            sch.to_svg(out, **opts)
            print(f'Escrito: {out}', file=sys.stderr)
    except Exception as exc:
        print(f'n2t: error de render: {exc}', file=sys.stderr)
        return EXIT_RENDER

    return EXIT_OK


def _cmd_lint(args) -> int:
    from .schematic import Schematic

    if not args.input.exists():
        print(f'n2t: error: archivo no encontrado: {args.input}',
              file=sys.stderr)
        return EXIT_IO

    try:
        sch = Schematic.from_file(args.input)
    except Exception as exc:
        print(f'n2t: parseo falló: {exc}', file=sys.stderr)
        return EXIT_PARSE

    n_elements = len(sch.elements)
    n_nodes = len(sch.nodes)
    print(f'OK: {args.input} ({n_elements} elementos, {n_nodes} nodos)',
          file=sys.stderr)
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.cmd == 'render':
        return _cmd_render(args)
    if args.cmd == 'lint':
        return _cmd_lint(args)

    parser.print_help(sys.stderr)
    return EXIT_IO


if __name__ == '__main__':
    sys.exit(main())
