# netlist2tikz

Generación de esquemáticos electrónicos en `circuitikz` (LaTeX) a
partir de netlists tipo SPICE. Es un **fork extractivo** de
[lcapy](https://github.com/mph-/lcapy) que conserva exclusivamente
el subsistema de dibujo, sin arrastrar el motor de análisis
simbólico.

```python
from netlist2tikz import Schematic

sch = Schematic("""
V1 1 0_1 ac; down
R1 1 2; right
Z1 2 3; right, l=Z_1
C1 3 0_3; down
W 0_1 0_3; right
; draw_nodes=connections
""")
sch.draw('circuito.pdf')
```

![](examples/09_impedancia_generica.png)

R, L y C se dibujan con el símbolo americano clásico (zigzag,
espiral, paralelas). Las impedancias genéricas usan `Z` (`Y` para
admitancias) y se dibujan como **rectángulo IEC**.

---

## Instalación

```bash
git clone git@github.com:javovelez/netlist2tikz.git
cd netlist2tikz
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Requisitos:

- Python ≥ 3.9
- `sympy`, `numpy`, `scipy` (se instalan automáticamente)
- Para renderizar a PDF/PNG/SVG: distribución LaTeX con `circuitikz`
  ≥ 1.4.5 disponible en `PATH`. En macOS con MacTeX o BasicTeX:
  `sudo tlmgr install circuitikz`.

Verificación rápida:

```bash
python -c "from netlist2tikz import Schematic; Schematic('R1 1 0; down').draw('/tmp/test.pdf')"
```

---

## Documentación

| Documento | Propósito |
|---|---|
| **[docs/REFERENCIA.md](docs/REFERENCIA.md)** | Catálogo exhaustivo de sintaxis: componentes, opciones por componente, opciones globales, formatos de salida. |
| **[docs/EJEMPLOS.md](docs/EJEMPLOS.md)** | Galería visual con ~25 circuitos curriculares de TCII (transitorios, resonancia, cuadripolos, transformadores, op-amps, filtros). |
| **[docs/ARQUITECTURA.md](docs/ARQUITECTURA.md)** | Cómo funciona internamente: pipeline parser → placer → emisor TikZ → pdflatex. Estructura de archivos, decisiones de diseño del fork. |

---

## Carpeta `examples/`

24 netlists curriculares listos para correr. Cada uno tiene su
`.sch` (fuente), `.pdf` (vectorial) y `.png`. Para regenerarlos:

```bash
python examples/render.py
```

Algunos destacados:

| Archivo | Tema |
|---|---|
| [01_resistor_simple.sch](examples/01_resistor_simple.sch) | Hola mundo |
| [03_rc_transitorio.sch](examples/03_rc_transitorio.sch) | Carga RC con escalón |
| [04_rlc_serie.sch](examples/04_rlc_serie.sch) | Resonante RLC serie |
| [09_impedancia_generica.sch](examples/09_impedancia_generica.sch) | Z rectángulo + R/C clásicos |
| [11_resonante_paralelo.sch](examples/11_resonante_paralelo.sch) | RLC paralelo con fuente de corriente |
| [12_fuente_VCCS.sch](examples/12_fuente_VCCS.sch) | VCCS (G) |
| [13_fuente_CCCS.sch](examples/13_fuente_CCCS.sch) | CCCS (F) |
| [15_opamp_integrador.sch](examples/15_opamp_integrador.sch) | Integrador con op-amp |
| [17_cuadripolo_T.sch](examples/17_cuadripolo_T.sch) | Cuadripolo en T |
| [18_cuadripolo_pi.sch](examples/18_cuadripolo_pi.sch) | Cuadripolo en π |
| [21_transformador_real.sch](examples/21_transformador_real.sch) | Transformador con fuga y resistencia de devanado |

Ver [docs/EJEMPLOS.md](docs/EJEMPLOS.md) para la galería completa
con vista previa.

---

## API mínima

```python
from netlist2tikz import Schematic

# Constructores explícitos
sch = Schematic.from_file('mi_circuito.sch')
sch = Schematic.from_string("R1 1 0; down\n")

# Salidas con extensión fija
sch.to_pdf('out.pdf')                # PDF vectorial
sch.to_png('out.png', dpi=600)       # PNG alta resolución
sch.to_svg('out.svg')                # SVG
sch.to_tikz()                        # → string TikZ standalone
sch.to_tikz(standalone=False)        # → solo \begin{tikzpicture}…

# Opciones globales como kwargs (anulan las del netlist)
sch.to_pdf('pelado.pdf',
           draw_nodes='none',
           label_nodes='none',
           label_ids=False,
           label_values=False)
```

El constructor genérico `Schematic(...)` y `sch.draw(filename)`
siguen funcionando (compatibilidad con docs/EJEMPLOS).

## CLI `n2t`

El paquete instala un binario `n2t`:

```bash
n2t render circuito.sch -o circuito.pdf       # formato por extensión
n2t render circuito.sch -o circuito.png --dpi 600
n2t render circuito.sch --tikz                # TikZ a stdout
n2t render circuito.sch --tikz --no-standalone > frag.tex
n2t render circuito.sch -o limpio.png --no-nodes --no-labels

n2t lint circuito.sch                          # exit 0 si parsea, 1 si no
```

Códigos de salida: `0` OK · `1` error de parseo · `2` error de render
(LaTeX/loop) · `3` I/O (archivo no encontrado, extensión desconocida).

Ver [docs/REFERENCIA.md §7](docs/REFERENCIA.md#7-cli-n2t) para detalles.

---

## Licencia y atribución

LGPL-2.1, heredada de lcapy. Ver [LICENCE](LICENCE) y [NOTICE](NOTICE).

Upstream: https://github.com/mph-/lcapy (Copyright 2014–2025 Michael
Hayes, UCECE).
