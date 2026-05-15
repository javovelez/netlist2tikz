# netlist2tikz

Convierte netlists tipo SPICE en código `circuitikz` (LaTeX) para dibujar
esquemáticos. Es un **fork extractivo** de [lcapy](https://github.com/mph-/lcapy)
que conserva exclusivamente el subsistema de dibujo, sin arrastrar el motor
de análisis simbólico.

## Instalación

```bash
pip install -e .
```

Requisitos:

- Python ≥ 3.9
- `sympy`, `numpy`, `scipy` (instalados automáticamente)
- Para renderizar a PDF/PNG/SVG: una distribución LaTeX con el paquete
  `circuitikz` ≥ 1.4.5 disponible en `PATH`.

## Uso básico

`Schematic` acepta dos formas:

```python
from netlist2tikz import Schematic

# Como string-netlist multilínea
sch = Schematic("""
R1 1 0; down
""")
sch.draw('resistencia.pdf')

# O como path a un archivo .sch
sch = Schematic('mi_circuito.sch')
sch.draw('mi_circuito.pdf')   # también .png, .svg, .tex
```

Nota: el motor de layout de lcapy requiere consistencia direccional. Si un
netlist mezcla orientaciones contradictorias el placer informa:
*"The horizontal schematic graph has a loop"*. Verificar las direcciones
(`down`/`right`/etc.) en cada línea.

## Licencia y atribución

Este proyecto deriva de `lcapy` (Copyright 2014–2025 Michael Hayes, UCECE)
y permanece bajo **GNU Lesser General Public License v2.1** (ver `LICENCE`).
Atribución detallada en `NOTICE`.

Upstream: https://github.com/mph-/lcapy
