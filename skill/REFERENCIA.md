# Referencia de sintaxis

Este documento describe **toda** la sintaxis que `netlist2tikz` entiende:
componentes, opciones por componente, opciones globales y notación de
etiquetas. Es la fuente canónica cuando se está construyendo o
revisando un netlist.

> **Nota sobre estilo**: por defecto se usa el estilo americano para
> R/L/C (zigzag, espiral, paralelas). Las **impedancias genéricas se
> dibujan como rectángulo** y se invocan con la letra `Z` (admitancias
> con `Y`). Para mostrar una impedancia rectangular junto a una
> resistencia clásica:
>
> ```
> R1 1 2; right, l=R_1
> Z1 2 3; right, l=Z_1
> ```

---

## 1. Anatomía de una línea

```
Nombre  N+  N-  [valor|expresión]  ;  opciones
```

| Campo | Obligatorio | Ejemplo |
|---|---|---|
| `Nombre` | sí | `R1`, `Vfuente`, `Z_eq` |
| Nodos `N+`, `N-` | sí (2 para bipolos; 3-4 para multipolos) | `1 0`, `2 0_2` |
| Valor / expresión | no | `1k`, `10`, `{V_th}`, `step 20` |
| `;` opciones | no | `; right=2, l=R_a, v_=V_R` |

Líneas que empiezan con `;` (sin nombre) son **opciones globales**
del schematic y suelen ir al final.

Convención de nodos:
- Los nombres son strings arbitrarios: `1`, `2`, `out`, `gnd`.
- `0` y derivados (`0_1`, `0_2`, etc.) se interpretan como tierra/referencia.
- Sufijo `_n` define un **sub-nodo** ortogonal al nodo principal — útil
  para forzar retornos de wire sin que el placer detecte loops
  horizontales.

---

## 2. Catálogo de componentes

### 2.1 Pasivos (2 terminales)

| Letra | Componente | Ejemplo | Forma |
|---|---|---|---|
| `R` | Resistencia | `R1 1 2 1k` | zigzag americano |
| `L` | Inductancia | `L1 1 2 10m` | espiral |
| `C` | Capacidad | `C1 1 2 100n` | paralelas |
| `Z` | **Impedancia genérica** | `Z1 1 2 Z_a` | **rectángulo** |
| `Y` | **Admitancia genérica** | `Y1 1 2 Y_a` | rectángulo |
| `W` | Cable / wire | `W 1 2` | línea (sin label) |
| `O` | Circuito abierto | `O 1 2` | gap |
| `P` | Puerto | `P1 1 0` | círculos en bornes |
| `D` | Diodo | `D1 1 2` | triángulo + barra |

### 2.2 Fuentes independientes

| Letra | Tipo | Ejemplo | Notas |
|---|---|---|---|
| `V` | Fuente de tensión | `V1 1 0 10` | DC por defecto |
| `V` (ac) | Tensión senoidal | `V1 1 0 ac` | senoidal genérica |
| `V` (escalón) | Tensión escalón | `V 1 0 step 20` | con valor de plateau |
| `I` | Fuente de corriente | `I1 0 1 1m` | nota la convención: la corriente entra por el nodo positivo |
| `I` (ac) | Corriente senoidal | `I1 0 1 ac` | |

### 2.3 Fuentes controladas (4 nodos)

| Letra | Tipo | Sintaxis | Significado |
|---|---|---|---|
| `E` | VCVS | `E1 n+ n- nc+ nc- mu` | v(n+,n-) = mu · v(nc+,nc-) |
| `F` | CCCS | `F1 n+ n- Vcontrol beta` | i = beta · i(Vcontrol) |
| `G` | VCCS | `G1 n+ n- nc+ nc- gm` | i = gm · v(nc+,nc-) |
| `H` | CCVS | `H1 n+ n- Vcontrol R` | v = R · i(Vcontrol) |

Para `F` y `H`, la corriente de control se mide a través de una fuente
de tensión nombrada (típicamente `V1` o un componente "ammeter" virtual).

Las fuentes controladas se dibujan como **rombos** con flecha (corriente)
o `+/-` (tensión).

### 2.4 Op-amp y amplificadores

El op-amp se modela como una `E` con el kind `opamp`:

```
E1 nout 0 opamp n+ n- A
```

Otros kinds disponibles para `E`:

| kind | Significado |
|---|---|
| `opamp` | Op-amp estándar (triángulo con + y -) |
| `fdopamp` | Op-amp totalmente diferencial |
| `inamp` | Amplificador de instrumentación |

### 2.5 Magnéticos

| Letra | Componente | Sintaxis | Ejemplo |
|---|---|---|---|
| `TF` | Transformador ideal | `TF n1+ n1- n2+ n2-` | `TF 1 0 2 0` |
| `TFcore` | Transformador con núcleo | `TF 1 0 2 0; core=true` | usa atributo |
| `TFtap` | Transformador con tap | `TFtap 1 0 2 0 3` | 5to nodo es el tap |
| `K` | Acoplamiento mutuo | `K L1 L2 0.9` | k entre dos inductores |

La relación de vueltas se anota con `l=`:
```
TF 1 0 2 0; right, l={N_1:N_2}
```

### 2.6 Interruptores

| Letra | Tipo | Ejemplo | Kinds |
|---|---|---|---|
| `SW` | Llave genérica | `SW1 1 2` | `no` (normally open), `nc` (normally closed), `spdt` |

### 2.7 Otros

| Letra | Componente |
|---|---|
| `Q` | Transistor BJT (3 terminales: colector, base, emisor) |
| `M` | Transistor MOSFET |
| `J` | Transistor JFET |
| `U` | Bloque de circuito integrado (chip genérico) |
| `A` | Anotación / símbolo |
| `BL` | Bloque funcional (filtro, mezclador, etc.) |
| `ANT` | Antena |
| `FB` | Ferrite bead |

---

## 3. Opciones por componente

Van después del `;` separadas por comas. Se pueden combinar libremente.

### 3.1 Dirección y tamaño

| Opción | Efecto |
|---|---|
| `right` | Horizontal hacia la derecha (default) |
| `left` | Horizontal hacia la izquierda |
| `up` | Vertical hacia arriba |
| `down` | Vertical hacia abajo |
| `right=N` | Derecha con largo N (en unidades de `node_spacing`) |
| `down=N`, etc. | Idem para otras direcciones |
| `size=N` | Largo sin cambiar dirección |
| `rotate=θ` | Ángulo arbitrario en grados (0 = derecha) |
| `scale=N` | Escala el componente (no la rama) |

> El placer **exige consistencia direccional**: si dos componentes
> implican que un nodo debe estar simultáneamente a izquierda y
> derecha de otro, el render falla con `RuntimeError: horizontal
> schematic graph has a loop`. Usar sub-nodos (`0_1`, `0_2`) y wires
> explícitos para evitarlo.

### 3.2 Reflexión

| Opción | Efecto |
|---|---|
| `mirror` | Espeja en el eje perpendicular a la rama |
| `invert` | Espeja en el eje de la rama |

### 3.3 Etiquetas del componente

| Opción | Posición | Ejemplo |
|---|---|---|
| `l=` | automática | `l=R_a` |
| `l_=` | abajo | `l_=10\\,\\Omega` |
| `l^=` | arriba | `l^=10k` |
| `l<=` | izquierda (en horizontal) | `l<=in` |
| `l>=` | derecha | `l>=out` |
| `a=`, `a_=`, `a^=` | anotación complementaria | `a=1\\,\\mathrm{k\\Omega}` |

### 3.4 Tensión y corriente

Las opciones `v=` y `v_=` agregan etiqueta de tensión con polaridad
implícita. Las `i=` y `i_=` agregan corriente.

| Opción | Significado |
|---|---|
| `v=`, `v_=`, `v^=` | Etiqueta de tensión (debajo / arriba) |
| `v<=`, `v>=` | Tensión con flecha de referencia |
| `i=`, `i_=`, `i^=` | Etiqueta de corriente |
| `i<`, `i>` | Flecha de corriente sin label |
| `i<=`, `i>=` | Etiqueta + flecha de corriente |
| `i^<=`, `i^>=` | Variantes con label arriba |
| `i_<=`, `i_>=` | Variantes con label abajo |

Ejemplos:
```
R1 1 2; right, v^=V_{R_1}        % V_{R_1} arriba del zigzag
L 2 3; right, i>^=I_L            % I_L con flecha hacia derecha, arriba
R2 3 0; down, v<=V_{R_2}         % polaridad invertida
```

### 3.5 Texto libre

| Opción | Efecto |
|---|---|
| `f=`, `f_=`, `f^=` | Etiqueta de texto libre sin convención de flecha |
| `f<=`, `f>=` | Etiqueta libre con flecha |

Útil para anotaciones tipo "primario", "carga", etc.

### 3.6 Estilo visual

| Opción | Efecto |
|---|---|
| `color=blue` | Color del componente (cualquier color de xcolor) |
| `thick` | Línea más gruesa |
| `dashed` | Línea punteada |
| `fill=red!20` | Relleno (para formas cerradas) |

### 3.7 Atributos específicos

| Opción | Aplica a | Ejemplo |
|---|---|---|
| `kind=` | D, Q, M, J, SW, BL | `kind=led`, `kind=nmos` |
| `core=true` | TF | núcleo dibujado |
| `nosim` | cualquiera | excluir de simulación (solo dibujo) |

---

## 4. Opciones globales del schematic

Se ponen en una línea que **empieza con `;`** (sin nombre de
componente), o como kwargs a `Schematic.draw(...)`.

### 4.1 Visibilidad de nodos

| Opción | Valores | Default | Efecto |
|---|---|---|---|
| `draw_nodes` | `all` / `none` / `primary` / `connections` | `primary` | qué nodos se dibujan como punto |
| `label_nodes` | `all` / `none` / `primary` / `alpha` | `none` | qué nodos se etiquetan con texto |

Convención:
- *primary*: nodos numéricos (`1`, `2`, …), no los sub-nodos `0_1`.
- *connections*: solo nodos con 3+ conexiones (uniones reales).
- *alpha*: solo nodos cuyo nombre empieza con letra (`in`, `out`).

### 4.2 Etiquetas de componentes

| Opción | Valores | Default | Efecto |
|---|---|---|---|
| `label_ids` | `True` / `False` | `True` | mostrar nombres (`R1`, `C1`, …) |
| `label_values` | `True` / `False` | `True` | mostrar valores (`1k`, `10\\,\\mu`) |
| `label_style` | `aligned` / `stacked` / `split` / `value` / `name` | `aligned` | disposición |
| `label_value_style` | `eng[N]` | `eng3` | precisión del formato ingeniería |
| `label_flip` | `True` / `False` | `False` | invierte arriba/abajo del label |

### 4.3 Estilo gráfico

| Opción | Valores | Default | Efecto |
|---|---|---|---|
| `style` | `american` / `british` / `european` | `american` | símbolo de R y L |
| `voltage_dir` | `RP` / `EF` | `RP` | convención de polaridad (RP = referencia pasiva) |
| `scale` | float | `1.0` | escala global |
| `node_spacing` | float | `2.0` | espaciado base entre nodos |
| `cpt_size` | float | `1.5` | tamaño base de componentes |
| `help_lines` | float | `0` | dibuja grilla (`0.5` para debug de layout) |
| `autoground` | bool | `False` | conecta automáticamente nodos `0` a tierra |
| `anchor` | str | varies | punto de anclaje del bounding box |

### 4.4 Notas sobre `style`

- `american` (default): R zigzag, L espiral, V/I con círculos.
- `european`: R rectángulo (IEC), L rectángulo con marcas. **Esto
  afecta a R, no a Z**. Si querés `R` clásica + `Z` rectángulo,
  dejá el estilo americano y usá `Z` para impedancias.
- `british`: variantes intermedias.

---

## 5. Notación de valores y expresiones

| Forma | Interpretación |
|---|---|
| `1k`, `2.2u`, `100n` | número + prefijo SI (k = 10³, u = 10⁻⁶, etc.) |
| `1e-6` | notación científica |
| `Meg` | mega (10⁶) — sufijo SPICE histórico |
| `R_a`, `Z_{eq}` | símbolo (no se formatea como valor) |
| `{expression}` | expresión sympy literal (uso especializado) |
| `step 20` | escalón unitario amplitud 20 (solo en V/I) |
| `ac` | fuente senoidal genérica |
| `ac 10 60` | senoidal de amplitud 10 a 60 Hz (rara vez usado para dibujo) |

Prefijos SI soportados: `f`, `p`, `n`, `u`, `m`, `k`, `M` (mega),
`G`, `T`. `Meg` también vale como alias de `M`.

---

## 6. Uso desde Python

### 6.1 Constructores

Tres formas equivalentes de cargar un netlist:

```python
from netlist2tikz import Schematic

# (a) Constructor genérico — adivina si la entrada es path o string-netlist
sch = Schematic('mi_circuito.sch')

# (b) Constructor explícito desde archivo — más claro y valida ruta
sch = Schematic.from_file('mi_circuito.sch')

# (c) Constructor explícito desde string — sin heurística
sch = Schematic.from_string("""
V1 1 0 ac; down
R1 1 2; right
C1 2 0_2; down
W 0 0_2; right
""")
```

Los classmethods `from_file` y `from_string` son la API recomendada
cuando se sabe exactamente qué tipo de entrada se tiene. Aceptan
`pathlib.Path` o `str`.

### 6.2 Salidas con extensión fija

Cuatro métodos con nombre que envuelven `draw()` y son más
descubribles:

```python
sch.to_pdf('salida.pdf')           # PDF vectorial
sch.to_png('salida.png', dpi=600)  # PNG a 600 dpi
sch.to_svg('salida.svg')           # SVG
sch.to_tikz()                      # string TikZ standalone (compilable)
sch.to_tikz(standalone=False)      # solo \begin{tikzpicture}…\end{tikzpicture}
```

Todos devuelven la ruta como string (o el contenido en el caso de
`to_tikz()`), útil para encadenar.

### 6.3 `draw()` genérico (compat)

El método `draw()` original sigue funcionando y elige el formato por
la extensión del archivo:

```python
sch.draw('rc.pdf')   # PDF
sch.draw('rc.png')   # PNG
sch.draw('rc.svg')   # SVG
sch.draw('rc.tex')   # solo TikZ standalone, sin compilar
```

### 6.4 Pasar opciones desde Python

Todas las opciones globales del schematic (sección 4) se aceptan
como kwargs y tienen prioridad sobre las del netlist:

```python
sch.to_pdf('rc.pdf',
           draw_nodes='none',
           label_nodes='none',
           label_ids=False,
           label_values=False,
           scale=0.8)
```

---

## 7. CLI `n2t`

El paquete instala un binario `n2t` con dos subcomandos:

```bash
n2t render INPUT.sch [-o OUTPUT] [--pdf|--png|--svg|--tikz] [opciones]
n2t lint   INPUT.sch
```

### 7.1 `n2t render`

Renderiza un netlist. Si `-o` tiene extensión conocida (`.pdf`,
`.png`, `.svg`, `.tex`), infiere el formato automáticamente.

```bash
# Inferencia por extensión (forma típica)
n2t render circuito.sch -o circuito.pdf
n2t render circuito.sch -o circuito.png --dpi 600
n2t render circuito.sch -o circuito.svg

# Formato explícito (cuando no hay -o)
n2t render circuito.sch --tikz                  # imprime a stdout
n2t render circuito.sch --tikz --no-standalone  # solo el bloque tikzpicture

# Flags de estilo
n2t render circuito.sch -o limpio.png --no-nodes --no-labels
n2t render circuito.sch -o europeo.pdf --style european --scale 0.8
```

Flags disponibles:

| Flag | Efecto |
|---|---|
| `-o`, `--output` | archivo de salida (sin `-o` y `--tikz` → stdout) |
| `--pdf` / `--png` / `--svg` / `--tikz` | fuerza formato (mutuamente excluyentes) |
| `--dpi N` | resolución del PNG (default 300) |
| `--style {american,british,european}` | estilo de símbolos |
| `--scale N` | escala global |
| `--no-nodes` | sin puntos ni etiquetas en los nodos |
| `--no-labels` | sin nombres ni valores de componentes |
| `--no-standalone` | con `--tikz`, emite solo el bloque tikzpicture |

### 7.2 `n2t lint`

Valida que el netlist se parsea sin errores. **No** detecta loops
topológicos (eso solo se ve al renderizar):

```bash
n2t lint circuito.sch
# OK: circuito.sch (5 elementos, 4 nodos)
```

### 7.3 Códigos de salida

| Código | Significado |
|---|---|
| `0` | OK |
| `1` | netlist inválido (error de parseo) |
| `2` | error de render (LaTeX falla, o el placer detecta loop) |
| `3` | error de I/O (archivo no existe, extensión desconocida, permisos) |

Útil para integrar en Makefiles o scripts de validación:

```makefile
%.pdf: %.sch
\tn2t render $< -o $@

validate:
\t@for f in *.sch; do n2t lint $$f || exit 1; done
```

---

## 8. Formatos de salida

| Extensión | Resultado |
|---|---|
| `.pdf` | PDF vectorial (recomendado para presentaciones) |
| `.png` | Mapa de bits (300 dpi por defecto) |
| `.svg` | SVG vectorial |
| `.tex` | Solo el código TikZ standalone (compilable) |
| `.sch` | Re-serializa el netlist (útil para normalización) |

El parámetro `dpi` controla la resolución de PNG:
```python
sch.draw('big.png', dpi=600)
```

---

## 9. Errores típicos y diagnóstico

### 8.1 `RuntimeError: horizontal schematic graph has a loop`

Significa que dos componentes implican posiciones contradictorias.
El mensaje (mejorado en este fork) incluye:

- el nodo donde se inició la traversal,
- los componentes que tocan ese nodo,
- los nodos alcanzados.

**Fix típico**: usar sub-nodos (`0_1`, `0_2`) en lugar de un único
nodo de tierra, y conectar con wires explícitos:

```
V1 1 0_1; down
R1 1 2; right
C1 2 0_2; down
W 0_1 0_2; right        % cierre explícito de tierra
```

### 8.2 `Undefined component '0' in 'P1 1 0.1; down'`

La notación de subnodos `0.1` (con punto) requiere componentes de tipo
`Shape` (chips, opamps). Para bipolos, usar `0_1` (con guión bajo).

### 8.3 `ValueError: Unsupported style: 'spice'`

`netlist2tikz` solo soporta la familia `eng` para formato de valores.
Removido en la limpieza de código muerto del fork.

---

## 10. Diferencias con lcapy upstream

`netlist2tikz` es un fork extractivo de
[lcapy](https://github.com/mph-/lcapy). Solo se conserva la
funcionalidad de **dibujo de esquemáticos** (netlist → TikZ →
LaTeX). Esto implica:

- No hay análisis simbólico (Laplace, Fourier, MNA).
- `Schematic` se importa directamente (`from netlist2tikz import Schematic`).
- `Circuit` no existe — usar `Schematic` con string-netlist.
- Estilos de formato de valor reducidos a `eng[N]`.
- `state.switch_context` / `state.restore_context` son no-ops.

La sintaxis de netlist es **100 % compatible** con lcapy, así que
los ejemplos del upstream funcionan tal cual.
