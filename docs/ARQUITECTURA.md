# Arquitectura interna

Documento técnico sobre **cómo** netlist2tikz convierte un netlist en
un PDF/PNG. Pensado para quien necesite extender el paquete, debuggear
un error oscuro o entender por qué tal o cual opción del netlist
produce tal o cual resultado.

Si solo querés usarlo, alcanza con la documentación de la skill:
[COMPONENTES.md](../skill/COMPONENTES.md), [PARAMETROS.md](../skill/PARAMETROS.md),
[INDICE.md](../skill/INDICE.md) y la [galería](../skill/galeria/README.md).

---

## 1. Pipeline en alto nivel

```
┌──────────────────┐    ┌──────────┐    ┌──────────────┐
│ string netlist   │───▶│ Parser   │───▶│ Schematic    │
│ "R1 1 0; down"   │    │ (regex)  │    │ (modelo)     │
└──────────────────┘    └──────────┘    └──────┬───────┘
                                               │
                                               ▼
            ┌────────────────────────────────────────────────────┐
            │ Schematic.draw(filename)                           │
            │                                                    │
            │  ┌──────────┐  ┌─────────┐  ┌──────────┐           │
            │  │ Placer   │─▶│ TikZ    │─▶│ LatexRunner          │
            │  │ (LP)     │  │ emitter │  │ (pdflatex)           │
            │  └──────────┘  └─────────┘  └────┬─────┘           │
            │                                  │                 │
            └──────────────────────────────────┼─────────────────┘
                                               ▼
                                       ┌──────────────┐
                                       │ PDF / PNG /  │
                                       │ SVG / TEX    │
                                       └──────────────┘
```

Cada paso vive en archivos separados del paquete:

| Etapa | Archivos principales |
|---|---|
| **Parseo** | `grammar.py`, `parser.py`, `netfile.py` |
| **Modelo** | `schematic.py`, `schemcpts.py`, `schematics/components/*.py` |
| **Placer** | `schemgraph.py`, `schemgraphplacer.py`, `schemlineqplacer.py`, `schemplacerbase.py` |
| **Emisor TikZ** | métodos `.draw()` de cada clase de componente, `schemcpts.py` |
| **Compilación** | `system.py` (`LatexRunner`, `PDFConverter`) |

---

## 2. Parseo del netlist

### 2.1 La gramática

[`grammar.py`](../netlist2tikz/grammar.py) define las reglas: cada letra
de prefijo (`R`, `L`, `C`, `V`, `I`, `E`, `F`, `G`, `H`, `K`, `TF`,
`P`, `W`, `O`, `Z`, `Y`, …) tiene una entrada con su número de nodos,
si acepta valor, kinds permitidos, etc.

La gramática es un dict de Python, no una EBNF formal. Cuando se
agrega un componente nuevo se agrega una entrada acá y una clase
en `schematics/components/`.

### 2.2 El parser

[`parser.py`](../netlist2tikz/parser.py) hace tokenización por regex
(`re.compile`) según las reglas de `grammar.py`. Para cada línea
distingue:

1. Nombre del componente y su tipo (por la letra inicial).
2. Lista de nodos.
3. Valor o expresión (opcional).
4. Opciones después del `;`.

Las opciones se parsean a un `Opts` (clase en `opts.py`) que es un
dict tipado.

### 2.3 El mixin de archivo

[`netfile.py`](../netlist2tikz/netfile.py) provee `NetfileMixin`, que
`Schematic` hereda. Es lo que permite leer desde un path o desde un
string. La heurística "string vs path" la implementa
[`schematic.py:119`](../netlist2tikz/schematic.py):

```python
if '\n' in filename or ';' in filename:
    # tratar como netlist literal
    ...
else:
    self.netfile_add(filename)
```

---

## 3. El modelo del schematic

### 3.1 Clase `Schematic`

[`schematic.py`](../netlist2tikz/schematic.py) define `Schematic`,
la fachada pública. Hereda `NetfileMixin`. Atributos importantes
después de parsear:

| Atributo | Tipo | Significado |
|---|---|---|
| `self.elements` | `OrderedDict[str, Cpt]` | componentes parseados, indexados por nombre |
| `self.nodes` | `dict[str, Node]` | nodos físicos del circuito |
| `self.node_spacing` | float | espaciado base (default 2.0) |
| `self.cpt_size` | float | tamaño base de componentes (default 1.2) |

### 3.2 Clases de componentes

Cada tipo de componente es una clase concreta. Jerarquía simplificada:

```
Cpt (schematics/components/cpt.py)
 ├── Bipole (2 terminales con valor)
 │    ├── Resistor (R)
 │    ├── Inductor (L)
 │    ├── Capacitor (C)
 │    ├── Impedance (Z) ← se dibuja como rectángulo (kind='generic')
 │    ├── Admittance (Y)
 │    ├── VoltageSource (V)
 │    ├── CurrentSource (I)
 │    └── ...
 ├── FixedCpt (multipolos con geometría fija)
 │    ├── Transformer (TF)
 │    ├── Transistor (Q, M, J)
 │    └── ...
 ├── Shape (chips, opamps)
 │    └── Eopamp, Efdopamp, ...
 ├── Wire (W)
 └── Unipole (P, ANT)
```

Cada clase implementa, entre otros:

| Método | Responsabilidad |
|---|---|
| `__init__(...)` | parsear sus args |
| `draw(...)` | emitir el fragmento TikZ |
| `node_pin_map` | mapeo nodos → puntos de anclaje en el componente |
| `coords` | coordenadas relativas de cada pin |

### 3.3 Por qué `Z` sale como rectángulo

`schemcpts.py:212-218` define `Impedance(Bipole)` con `cpt_kind='generic'`.
Ese kind se traduce, al emitir TikZ, en `\draw ... to [generic] ...`,
que es el rectángulo de circuitikz. R, L, C usan kinds americanos
(`resistor`, `inductor`, `capacitor`).

El estilo global `american`/`british`/`european` se inyecta solo
sobre los kinds que tienen variantes — no sobre `generic`, por eso
`Z` permanece rectangular en todos los estilos.

---

## 4. El placer (layout)

Aquí ocurre la parte interesante: a partir de los componentes con sus
direcciones (`right`, `down`, etc.) hay que asignar coordenadas
(x, y) a cada nodo.

### 4.1 El problema

Cada línea del netlist define una **rama** entre dos nodos con una
**dirección** y un **largo** (potencialmente flexible).
Matemáticamente, hay que resolver un sistema de restricciones lineales:

- Si `R1 1 2; right`, entonces `x_2 - x_1 = size_R1`, `y_2 = y_1`.
- Si `C1 2 0_2; down`, entonces `y_{0_2} - y_2 = -size_C1`, `x_{0_2} = x_2`.
- Y así para cada componente.

El sistema puede ser:
- **Sobredeterminado** (loop inconsistente) → `RuntimeError`.
- **Subdeterminado** (cadenas libres) → se resuelven con tamaños default.
- **Bien planteado** → solución única.

### 4.2 Dos placers en serie

[`schemplacer.py`](../netlist2tikz/schemplacer.py) elige entre dos
algoritmos:

1. **`SchemGraphPlacer`** ([schemgraphplacer.py](../netlist2tikz/schemgraphplacer.py)):
   construye un DAG por dirección (uno horizontal, uno vertical) y
   propaga distancias. Es el placer "rápido" y maneja la mayoría de
   casos.
2. **`SchemLineqPlacer`** ([schemlineqplacer.py](../netlist2tikz/schemlineqplacer.py)):
   plantea el problema como sistema de ecuaciones lineales y lo
   resuelve con `scipy.linalg`. Más general pero más caro.

El grafo del placer se construye en [`schemgraph.py`](../netlist2tikz/schemgraph.py).
Cada nodo del netlist se convierte en un `Gnode` con `.fedges`
(salientes), `.redges` (entrantes), `.pos` (posición asignada).

### 4.3 Detección de loops

El placer detecta inconsistencias en `path_to_closest_known` y
`path_to_furthest` ([schemgraph.py:687-731](../netlist2tikz/schemgraph.py#L687)).
Cuando la recursión excede 1000 niveles asume loop y lanza
`RuntimeError`.

En este fork el mensaje del error fue **mejorado** para incluir el
nodo donde se inició la traversal, los componentes que lo tocan, y
los nodos alcanzados. Ver
[schemgraph.py:725-749](../netlist2tikz/schemgraph.py#L725).

### 4.4 Convenciones de sub-nodos

La convención `0`, `0_1`, `0_2` no es magia del placer: son
**identificadores de nodos distintos** que el usuario marca como
"misma red eléctrica" mediante wires (`W 0_1 0_2`). El placer no
los unifica geométricamente — eso permite cerrar mallas
controladamente sin ambigüedad de posición.

---

## 5. Emisión del TikZ

Una vez resueltas las posiciones, `Schematic._tikz_draw()` itera
sobre cada `Cpt.draw(...)` para componer el string TikZ.

El template incluye:

```latex
\documentclass[tikz]{standalone}
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american voltages]   % o european, según opción global
  \draw (0,0) to[R, l=R_1] (2,0);
  \draw (2,0) to[L, l=L_1] (4,0);
  ...
\end{circuitikz}
\end{document}
```

El bloque `american voltages` / `european voltages` proviene de la
opción global `style`. Los estilos por componente (`kind=led`, etc.)
se traducen a opciones del `\draw[to[...]]`.

Las etiquetas usan macros de circuitikz: `l=`, `l_=`, `l^=`, `i=`,
`v=`, etc. Hay también formateo de valores con prefijos SI (`1k` →
`1\,\mathrm{k}\Omega`) que ocurre en
[`valueformatter.py`](../netlist2tikz/valueformatter.py) (clase
`EngValueFormatter`).

---

## 6. Compilación a PDF/PNG/SVG

[`system.py`](../netlist2tikz/system.py) tiene dos helpers:

| Clase | Función |
|---|---|
| `LatexRunner` | invoca `pdflatex` (o `lualatex`) sobre el .tex generado |
| `PDFConverter` | convierte PDF → PNG (vía `pdftoppm`) o SVG (vía `pdf2svg`) |

El flujo para `sch.draw('out.png')`:

1. Generar `out.tex` en `tmpfilename()` (suele ser `/var/folders/.../tmp_xxx.tex`).
2. `pdflatex out.tex` → `out.pdf`.
3. `pdftoppm -r 300 out.pdf out` → `out-1.png`.
4. Renombrar a `out.png`, limpiar temporales.

Si solo se pide `.tex` (extensión `.tex` o `.sch`), se salta `pdflatex`
y queda el código TikZ standalone, listo para `\input{}` en otro
documento.

---

## 7. Estructura del paquete

```
netlist2tikz/
├── netlist2tikz/              ← paquete Python
│   ├── __init__.py            ← expone Schematic
│   ├── schematic.py           ← clase principal
│   ├── schemcpts.py           ← clases de componentes (mapeo letra → clase)
│   ├── schematics/
│   │   ├── utils.py
│   │   └── components/
│   │       ├── bipole.py      ← R, L, C, V, I, Z, Y, D, ...
│   │       ├── opamp.py       ← Eopamp, Einamp, ...
│   │       ├── transformer.py ← TF, K
│   │       ├── transistor.py  ← Q, M, J
│   │       ├── shape.py
│   │       └── ...
│   ├── grammar.py             ← reglas de parseo
│   ├── parser.py              ← parser por regex
│   ├── netfile.py             ← NetfileMixin (string vs path)
│   ├── opts.py                ← parser de opciones (clave=valor)
│   ├── rcparams.py            ← config con defaults
│   ├── rcdefaults.py          ← valores por defecto + checkers
│   ├── rcchecker.py           ← validación de tipos en rcparams
│   ├── schemgraph.py          ← DAG del placer
│   ├── schemgraphplacer.py    ← placer rápido (BFS sobre el DAG)
│   ├── schemlineqplacer.py    ← placer general (sistema lineal)
│   ├── schemplacer.py         ← dispatcher entre los dos placers
│   ├── schemplacerbase.py     ← código común a placers
│   ├── schemmisc.py           ← Pos, Steps (helpers de geometría)
│   ├── schemnode.py           ← clase Node del schematic
│   ├── label.py               ← clase Label
│   ├── labels.py              ← collection de Labels
│   ├── labelmaker.py          ← genera labels desde un Cpt
│   ├── latex.py               ← helpers latex (mathrm de subscripts)
│   ├── valueformatter.py      ← prefijos SI / notación ingeniería
│   ├── valueparser.py         ← parseo de valores tipo "42p", "100k"
│   ├── system.py              ← LatexRunner, PDFConverter
│   ├── state.py               ← stub no-op (era contexto sympy)
│   ├── attrdict.py            ← dict con acceso por atributo
│   ├── cnodes.py              ← nodos conectados (helper de placer)
│   ├── componentnamer.py      ← genera nombres únicos para componentes anónimos
│   ├── config.py              ← constantes globales
│   ├── immittancemixin.py     ← stub vacío (era análisis de impedancia)
│   ├── node.py                ← clase Node de bajo nivel
│   └── nodes.py               ← parse_nodes (resuelve sub-nodos)
├── tests/                     ← smoke tests
├── examples/                  ← galería de circuitos (.sch + render.py)
├── docs/                      ← este directorio
├── LICENCE                    ← LGPL-2.1 (heredada de lcapy)
├── NOTICE                     ← atribución a Michael Hayes / UCECE
├── README.md
└── pyproject.toml             ← deps: sympy, numpy, scipy
```

---

## 8. Decisiones de diseño del fork

Este paquete es una **extracción quirúrgica** de
[lcapy](https://github.com/mph-/lcapy). Las decisiones que vale la
pena conocer si vas a tocar el código:

### 8.1 Por qué `sympy` sigue siendo dependencia

El usuario pasa expresiones simbólicas como valor de componente
(ej. `R1 1 2 R_a`). Para imprimirlas correctamente en LaTeX
(`R_a` → `R_a$`) hay que sympificarlas. `transformer.py` también
las usa para decidir signos. Quitar sympy implicaría reescribir esa
lógica.

### 8.2 Los stubs vacíos `equation.py`, `expr.py`

(eliminados en la limpieza de código muerto — solo existían para que
los `isinstance()` de `printing.py` no fallaran. Ya no son necesarios
porque `printing.py` también fue eliminado.)

### 8.3 `state` reducido a no-ops

Lcapy usa `state.switch_context()` para gestionar contextos de
símbolos sympy. Como acá no analizamos simbólicamente, las dos
llamadas que sobreviven son no-ops definidas en `state.py`.

### 8.4 Reescritura de `labelmaker.py`

El upstream usaba `lcapy.expr.Expr` para envolver expresiones. En
este fork se usa `sympy.latex` y `sympy.sympify` directamente. Es
más simple y elimina una dependencia interna.

### 8.5 Mensajes de error de loop mejorados

Los tres `RuntimeError` de [schemgraph.py](../netlist2tikz/schemgraph.py)
(loop horizontal, dodgy x2) ahora incluyen el nodo, los componentes
que lo tocan y los nodos alcanzados. El upstream solo decía "the
schematic graph has a loop".

---

## 9. Cómo extender

### 9.1 Agregar un componente nuevo

Pasos:

1. Agregar la regla en [`grammar.py`](../netlist2tikz/grammar.py): letra,
   número de nodos, si acepta valor, kinds permitidos.
2. Crear la clase en `schematics/components/` (heredar `Bipole`,
   `FixedCpt`, o `Shape` según corresponda). Implementar `draw()`.
3. Registrar en [`schemcpts.py`](../netlist2tikz/schemcpts.py): mapeo
   letra → clase.
4. Agregar un test smoke en `tests/` y un ejemplo en `examples/`.

### 9.2 Agregar una opción global nueva

1. Default en [`rcdefaults.py`](../netlist2tikz/rcdefaults.py).
2. Si requiere validación, definir un checker en
   [`rcchecker.py`](../netlist2tikz/rcchecker.py).
3. Consumir desde donde corresponda (típicamente en
   `Schematic._tikz_draw()` o en una clase de componente).

### 9.3 Cambiar el algoritmo de layout

Ver [schemplacer.py](../netlist2tikz/schemplacer.py): es un dispatcher
trivial entre los dos placers existentes. Se puede agregar uno
nuevo implementando la misma interfaz (`solve(spacing)`).

---

## 10. Tests

Hay smoke tests en [tests/test_smoke.py](../tests/test_smoke.py) que
validan:

- Que `Schematic` se puede importar.
- Que un netlist se parsea (con elementos esperados en `sch.elements`).
- Que un divisor simple no rompe el parser.

Para tests más amplios (golden snapshots del TikZ, validación de
componentes individuales), ver la sección "Fuera de scope" del plan
en `/Users/javiervelez/.claude/plans/`.

Una verificación end-to-end manual es correr
`python examples/render.py` y revisar que los 24 PDFs/PNGs se
generen sin errores.
