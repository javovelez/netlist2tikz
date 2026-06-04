---
name: netlist2tikz
description: Dibuja esquemáticos eléctricos en circuitikz/TikZ a partir de descripciones en lenguaje natural o de netlists tipo SPICE. Útil para materiales de cátedra (Teoría de Circuitos II, Análisis de Señales y Sistemas) con circuitos R/L/C clásicos, impedancias genéricas como rectángulo, transformadores, fuentes controladas, opamps, filtros y cuadripolos. Usar cuando el usuario pida "dibujá un circuito", "renderizá un esquemático", "hacé un filtro RC", "armá un divisor de tensión", "esquemático de un transformador", o cualquier descripción de un circuito eléctrico/electrónico que requiera una imagen.
allowed-tools: Bash, Read, Write, Edit
---

# Skill: netlist2tikz

Generás esquemáticos circuitikz/TikZ a partir de descripciones del usuario,
usando el paquete Python `netlist2tikz` y su CLI `n2t`.

## Tu objetivo

Cuando el usuario describe un circuito (con palabras o pidiendo modificar un netlist):

1. **Generá un netlist** acorde a la descripción.
2. **Renderizalo a PDF y PNG** en una ruta razonable (preguntá si no es obvio).
3. **Mostrá el resultado** (PNG inline si se puede, o ruta absoluta al PDF).
4. **Iterá** si el usuario pide cambios.

## Convenciones del autor (importante)

- **R, L, C con símbolo americano clásico** (zigzag, espiral, paralelas): no cambies
  a `european` salvo pedido explícito.
- **Impedancias genéricas como rectángulo**: usar el componente `Z` (no `R` europea).
  Ej: `Z1 1 2; right, l=Z_1`. Admitancias con `Y`.
- **Idioma español**. Las etiquetas respetan la notación del enunciado (`V_1`, `I_o`,
  `Z_a`, `5 I_1`, `30·I_1`, …) tal como vienen.
- **Coma decimal** en texto explicativo (en el netlist los valores usan punto: `1.5k`).

## Protocolo de búsqueda (cómo encontrar info rápido)

La documentación está organizada para **buscar con `rg`**. No leas archivos enteros:
ubicá el `id` y leé sólo esa ficha.

1. **¿Entra en el cheatsheet de abajo?** → resolvé directo.
2. **Si no**, despachá por [INDICE.md](INDICE.md):
   ```bash
   rg -i "<palabra>" skill/INDICE.md          # intención → id (cpt-… / param-… / gl-…)
   rg "id: <id>" skill/COMPONENTES.md skill/PARAMETROS.md   # leer la ficha exacta
   ```
3. **¿Querés un circuito parecido?** buscá en la galería por tag/componente:
   ```bash
   rg -l "n2t-tags:.*resonancia" skill/galeria/sch/   # ejemplos con ese tag
   rg -l "cpt:tf" skill/galeria/sch/                  # ejemplos que usan transformador
   ```
   y adaptá el `.sch` más cercano. Índice máquina: `skill/galeria/index.tsv`.

| archivo | para qué |
|---|---|
| [INDICE.md](INDICE.md) | despacho intención→id, vocabulario de tags, ruta curricular |
| [COMPONENTES.md](COMPONENTES.md) | ficha de cada componente (`cpt-*`) |
| [PARAMETROS.md](PARAMETROS.md) | ficha de cada parámetro modificable (`param-*`, `gl-*`) |
| [galeria/](galeria/README.md) | ~520 ejemplos espejados de lcapy + curriculares, con miniaturas |

## Cómo invocar el paquete

El paquete vive en un venv del repo. Hay que resolver la ruta del repo y usar el
`n2t` y el python de ese venv.

### Resolución del path del repo (una vez por sesión)

La carpeta de la skill (`~/.claude/skills/netlist2tikz`) es un **symlink** a `<REPO>/skill`:

```bash
REPO="$(dirname "$(dirname "$(readlink -f "$HOME/.claude/skills/netlist2tikz")")")"
echo "$REPO"
```
(En macOS sin `readlink -f`: `realpath` o `python3 -c "import os;print(os.path.realpath('$HOME/.claude/skills/netlist2tikz/..'))"`.)

Verificá el venv: `ls "$REPO/.venv/bin/n2t"`. Si **no** existe, pedile al usuario:
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -e .
```

### Opción A: CLI (preferida)

```bash
"$REPO/.venv/bin/n2t" render circuito.sch -o circuito.pdf
"$REPO/.venv/bin/n2t" render circuito.sch -o circuito.png --dpi 300
"$REPO/.venv/bin/n2t" render circuito.sch --tikz                 # TikZ a stdout
"$REPO/.venv/bin/n2t" render circuito.sch --tikz --no-standalone # solo el bloque tikzpicture
"$REPO/.venv/bin/n2t" render circuito.sch -o limpio.png --no-nodes --no-labels
"$REPO/.venv/bin/n2t" lint circuito.sch
```
Códigos de salida: `0` OK · `1` parseo · `2` render (LaTeX o loop) · `3` I/O.

### Opción B: Python API (varias salidas / composición)

```bash
"$REPO/.venv/bin/python" -c '
from netlist2tikz import Schematic
sch = Schematic.from_string("R1 1 0; down\n")
sch.to_pdf("/tmp/c.pdf"); sch.to_png("/tmp/c.png", dpi=300)
print(sch.to_tikz(standalone=False))
'
```

## Cheatsheet (el 90% de los casos)

Cada línea: `Nombre N+ N- [valor]; opciones`. Catálogo completo → COMPONENTES.md / PARAMETROS.md.

### Componentes más usados

| Letra | Componente | Forma | Ejemplo |
|---|---|---|---|
| `R` `L` `C` | resistencia/inductancia/capacidad | zigzag/espiral/paralelas | `R1 1 2 1k; right` |
| `Z` `Y` | **impedancia/admitancia genérica** | **rectángulo** | `Z1 1 2; right, l=Z_a` |
| `V` `I` | fuente tensión/corriente | círculo | `V1 1 0 ac; down` · `V 1 0 step 20` |
| `W` `O` `P` | cable / abierto / puerto | línea / gap / bornes | `W 0_1 0_2; right` |
| `E` `F` `G` `H` | VCVS / CCCS / VCCS / CCVS | rombo | `E1 o 0 opamp + - A` |
| `TF` `K` | transformador / acoplamiento | espiras | `TF 1 0 2 0; right, l={N_1:N_2}` |
| `TP` `TPZ…` | cuadripolo caja / con parámetros | rectángulo | `TP1 1 2 3 4; right, l=Red` |
| `D` `Q` `M` `J` `SW` | diodo/BJT/MOSFET/JFET/llave | — | `D1 1 2; right, kind=zener` |

### Direcciones, etiquetas, nodos (lo más usado)

| Opción | Efecto |
|---|---|
| `right`/`left`/`up`/`down` (`=N`) | dirección (+ largo N) |
| `size=N` · `rotate=θ` · `mirror`/`invert` | largo / ángulo / espejo |
| `l=` `l^=` `l_=` | etiqueta (auto/arriba/abajo) |
| `v=` `v^=` `v_=` | etiqueta de tensión |
| `i=` `i>^=` `i<^=` | etiqueta/flecha de corriente |
| `color=blue` `thick` `dashed` | estilo |

### Visibilidad de nodos (globales, línea que empieza con `;`)

```
; draw_nodes=connections, label_nodes=primary, label_ids=False, scale=0.8
```

| Global | Valores | Default |
|---|---|---|
| `draw_nodes` | all / none / primary / connections / labeled | **`labeled`** |
| `label_nodes` | all / none / primary / alpha | **`none`** |
| `label_ids` · `label_values` | True/False | `True` |
| `style` | american / british / european | `american` |
| `voltage_dir` | RP (pasiva) / EF (activa) | `RP` |
| `scale` · `node_spacing` · `cpt_size` | float | 1.0 / **1.2** / 1.5 |
| `font` | comando LaTeX | `\fontsize{7.5}{9}\selectfont` (−25%); `; font=\normalsize` para tamaño pleno |

Detalle y todos los demás parámetros → `PARAMETROS.md` (grep `id: gl-…`).
**Defaults del fork** (dibujos limpios y compactos para cátedra): `draw_nodes=labeled` (punto solo en puertos/terminales o nodos etiquetados), `label_nodes=none`, `node_spacing=1.2`, fuente −25%. No hace falta agregar `; draw_nodes=…, label_nodes=…` en cada netlist.

## Labels con comas internas (importante)

Secuencias LaTeX con coma (`\,` espacio fino, `\;`, `\:`, `\!`) y coma decimal `{,}`
se preservan sin envolver en llaves:
```
V1 1 0; down, l=5\,I_1            # 5 [espacio fino] I_1
R2 4 0; down, l=16{,}2\,V_a       # 16,2 V_a (coma decimal española)
V3 1 0; down, l=0{,}0395\,V_1
```
Si un PDF sale < ~2 KB con warning de "PDF sospechosamente chico" → label mal escapada.
(Ficha: `id: lbl-comas` en PARAMETROS.md.)

## Patrones que funcionan (anti-loop)

El placer es **estricto con la consistencia direccional**. Si dos componentes implican
que un nodo esté a izquierda y derecha a la vez → `RuntimeError: ... graph has a loop`.

**Patrón canónico para cerrar mallas**: sub-nodos (`0_1`, `0_2`) + wires explícitos.

✅ Bien:
```
V1 1 0_1; down
R1 1 2; right=2
R2 2 0_2; down
W 0_1 0_2; right=2
```
❌ Mal (loop): `V1 1 0; down / R1 1 2; right / R2 2 0; down` (el `0` queda a izq y der).

## Few-shot: descripción → netlist

**"R y C en serie alimentados por fuente AC"**
```
V1 1 0_1 ac; down
R1 1 2; right
C1 2 0_2; down
W 0_1 0_2; right
; draw_nodes=connections
```

**"Divisor de tensión 10 V con R1=1k y R2=2k"**
```
V1 1 0_1 10; down
R1 1 2 1k; right=2.5
R2 2 0_2 2k; down=2
W 0_1 0_2; right=2.5
; draw_nodes=connections, label_nodes=primary
```

**"Cuadripolo en T con impedancias Z_a, Z_b, Z_c"**
```
P1 1 0; down, v_=V_1
Z1 1 2; right=2, i>^=I_1, l=Z_a
Z2 2 0_2; down=1.5, l=Z_b
Z3 2 3; right=2, i^<=I_2, l=Z_c
W 0 0_2; right
P2 3 0_3; down, v=V_2
W 0_2 0_3; right
; draw_nodes=connections, label_nodes=primary
```

**"Cuadripolo como caja negra 'Red R'"** (sin topología interna → `TP`, no Z en T/π)
```
TP1 1 2 3 4; right, l=Red\ R
W 1 1a; right=0.5, i^<=I_2
W 3a 3; right=0.5, i=I_1
P 1a 2a; down, v^=V_2
P 3a 4a; down, v_=V_1
; draw_nodes=none, label_nodes=none
```
Variantes con parámetros: `TPZ`/`TPY`/`TPH`/`TPA`/`TPB`/`TPG`. Nube: `shape=cloud`.

Más patrones → buscá en la galería (`rg -l "cpt:tp" skill/galeria/sch/`, etc.).

## Workflow recomendado

1. **Algo conocido** (RC, RLC, divisor, cuadripolo…) → buscá un ejemplo cercano en la
   galería (`rg -l "n2t-tags:.*<tema>" skill/galeria/sch/`) y adaptalo. Los del tema
   `00_curricular` ya son loop-safe y con las convenciones del autor.
2. **Algo nuevo** → generá el netlist, validá con `n2t lint /tmp/x.sch`, después renderizá.
3. **Falla con loop** → leé el error (nombra los componentes culpables) y usá sub-nodos.
4. **Cambios** → modificá el netlist existente, no regeneres de cero.

## Salidas

Por defecto generá **PDF + PNG** en una carpeta sensata (`/tmp/<nombre>.{pdf,png}` si no
hay ruta). El PNG sirve para mostrar inline; el PDF para integrar en LaTeX.

Si el usuario quiere el TikZ para sus apuntes / Overleaf:
```bash
n2t render circuito.sch --tikz --no-standalone > circuito_frag.tex   # solo tikzpicture
n2t render circuito.sch --tikz > circuito.tex                        # documento standalone
```
