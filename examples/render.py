"""Renderiza todos los .sch del directorio a PDF y PNG."""

import sys
import traceback
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=SyntaxWarning)

from netlist2tikz import Schematic


def render_one(sch_path: Path, fmt: str) -> str:
    target = sch_path.with_suffix('.' + fmt)
    try:
        Schematic(str(sch_path)).draw(str(target))
    except Exception as exc:
        return f'ERROR: {exc.__class__.__name__}: {exc}'
    if target.exists():
        return f'{target.name} ({target.stat().st_size} B)'
    return 'no se generó archivo'


def main() -> int:
    here = Path(__file__).parent
    sch_files = sorted(here.glob('*.sch'))
    if not sch_files:
        print('No hay .sch en', here)
        return 1

    failures = 0
    for sch in sch_files:
        print(f'== {sch.name} ==')
        for fmt in ('pdf', 'png'):
            result = render_one(sch, fmt)
            print(f'  {fmt}: {result}')
            if result.startswith('ERROR') or result == 'no se generó archivo':
                failures += 1

    print()
    print(f'Total: {len(sch_files)} netlists, {failures} fallos.')
    return 0 if failures == 0 else 2


if __name__ == '__main__':
    sys.exit(main())
