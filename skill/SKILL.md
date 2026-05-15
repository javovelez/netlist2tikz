---
name: netlist2tikz
description: Dibuja esquemáticos eléctricos en circuitikz/TikZ a partir de descripciones en lenguaje natural o de netlists tipo SPICE. Útil para materiales de cátedra (Teoría de Circuitos II, Análisis de Señales y Sistemas) con circuitos R/L/C clásicos, impedancias genéricas como rectángulo, transformadores, fuentes controladas, opamps, filtros y cuadripolos. Usar cuando el usuario pida "dibujá un circuito", "renderizá un esquemático", "hacé un filtro RC", "armá un divisor de tensión", "esquemático de un transformador", o cualquier descripción de un circuito eléctrico/electrónico que requiera una imagen.
allowed-tools: Bash, Read, Write, Edit
---

# Skill: netlist2tikz

Generás esquemáticos circuitikz/TikZ a partir de descripciones del usuario,
usando el paquete Python `netlist2tikz` y su CLI `n2t`.

## Tu objetivo

Cuando el usuario describe un circuito (ya sea con palabras o pidiendo
modificar un netlist existente):

1. **Generá un netlist** acorde a la descripción.
2. **Renderizalo a PDF y PNG** en una ruta razonable (preguntá si no es obvio).
3. **Mostrá el resultado** al usuario (PNG inline si el entorno lo permite,
   o ruta absoluta al PDF).
4. **Iterá** si el usuario pide cambios (más componentes, otro estilo, etc.).

## Convenciones del autor (importante)

- **R, L, C con símbolo americano clásico** (zigzag, espiral, paralelas):
  no cambies a `european` salvo pedido explícito.
- **Impedancias genéricas como rectángulo**: usar el componente `Z`
  (no `R` con `style=european`). Ejemplo: `Z1 1 2; right, l=Z_1`.
- **Idioma**: español. Etiquetas de circuitos respetan la notación del
  enunciado del usuario (mantené `V_1`, `I_o`, `Z_a`, etc. como vienen).
- **Coma decimal** en valores numéricos cuando aparezca en texto explicativo
  (no en el netlist, donde se usa punto: `1.5k`).

## Cómo invocar el paquete

El paquete `netlist2tikz` está instalado en modo editable dentro de un
venv del repo. Para que la skill funcione, hace falta resolver la ruta
del repo y usar el binario `n2t` y el python de ese venv.

### Resolución del path del repo (una vez por sesión)

La carpeta de la skill (`~/.claude/skills/netlist2tikz`) es un **symlink**
a `<REPO>/skill`. Para obtener `<REPO>`:

```bash
REPO="$(dirname "$(dirname "$(readlink -f "$HOME/.claude/skills/netlist2tikz")")")"
echo "$REPO"
# /Users/javiervelez/Library/CloudStorage/.../netlist2tikz
```

(En macOS sin `readlink -f`, usar `realpath` o `python -c "import os; print(os.path.realpath('$HOME/.claude/skills/netlist2tikz/..'))"`.)

Verificá que el venv exista: `ls "$REPO/.venv/bin/n2t"`. Si **no** existe,
decile al usuario que corra desde la raíz del repo:

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -e .
```

### Opción A: CLI (preferida para tareas simples)

```bash
# Asumiendo $REPO resuelto como arriba
"$REPO/.venv/bin/n2t" render circuito.sch -o circuito.pdf
"$REPO/.venv/bin/n2t" render circuito.sch -o circuito.png --dpi 300
"$REPO/.venv/bin/n2t" render circuito.sch --tikz
"$REPO/.venv/bin/n2t" render circuito.sch --tikz --no-standalone
"$REPO/.venv/bin/n2t" render circuito.sch -o limpio.png --no-nodes --no-labels
"$REPO/.venv/bin/n2t" lint circuito.sch
```

Códigos de salida: 0=OK, 1=parseo, 2=render (LaTeX o loop), 3=I/O.

### Opción B: Python API (cuando hace falta múltiples salidas o composición)

```bash
"$REPO/.venv/bin/python" -c '
from netlist2tikz import Schematic
sch = Schematic.from_string("R1 1 0; down\n")
sch.to_pdf("/tmp/circuito.pdf")
sch.to_png("/tmp/circuito.png", dpi=300)
print(sch.to_tikz(standalone=False))
'
```

## Sintaxis del netlist (cheatsheet)

Cada línea: `Nombre N+ N- [valor]; opciones`.

### Componentes más usados

| Letra | Componente | Forma | Ejemplo |
|---|---|---|---|
| `R` | resistencia | zigzag | `R1 1 2 1k; right` |
| `L` | inductancia | espiral | `L1 2 3 10m; right` |
| `C` | capacidad | paralelas | `C1 3 0 100n; down` |
| `Z` | **impedancia genérica** | **rectángulo** | `Z1 1 2; right, l=Z_a` |
| `Y` | admitancia genérica | rectángulo | `Y1 1 2; right, l=Y_a` |
| `V` | fuente tensión | círculo | `V1 1 0 ac; down` o `V 1 0 step 20` |
| `I` | fuente corriente | círculo | `I1 0 1 ac; up` |
| `W` | wire (cable) | línea | `W 0_1 0_2; right` |
| `O` | circuito abierto | gap | `O 1 2; right` |
| `P` | puerto | círculos vacíos | `P1 1 0; down, v=V_1` |
| `TF` | transformador | dos espirales | `TF 1 0 2 0; right, l={N_1:N_2}` |
| `TP` | **cuadripolo caja negra** | **rectángulo con texto** | `TP1 1 2 3 4; right, l=Red\\ R` |
| `TPZ`, `TPY`, `TPH`, `TPA`, `TPB`, `TPG` | cuadripolo con parámetros nombrados | rectángulo etiquetado | `TPZ 1 2 3 4; right` (etiqueta automática TP_Z) |
| `E` | VCVS (también opamp) | rombo / triángulo | `E1 out 0 opamp inp inm A` |
| `F` | CCCS | rombo | `F1 1 0 V1 beta; down` |
| `G` | VCCS | rombo | `G1 1 0 nc+ nc- gm; down` |
| `H` | CCVS | rombo | `H1 1 0 V1 R; down` |

> **Cuadripolos `TP*`**: la sintaxis es `TPname n1+ n1- n2+ n2-` (4 nodos
> en orden: puerto-1+, puerto-1-, puerto-2+, puerto-2-). Acepta `shape=cloud`
> para dibujar como nube en lugar de rectángulo (útil para "red indefinida").
> Distinto del cuadripolo construido con impedancias `Z` en topología T o π
> (que muestra la estructura interna).

### Direcciones y tamaños (después del `;`)

| Opción | Efecto |
|---|---|
| `right`, `left`, `up`, `down` | dirección |
| `right=N` (etc.) | dirección + largo N |
| `size=N` | sólo largo (sin cambiar dirección) |
| `mirror` / `invert` | espejo |
| `rotate=θ` | ángulo en grados |

### Etiquetas

| Opción | Efecto |
|---|---|
| `l=...` | label automático |
| `l_=`, `l^=` | label abajo / arriba |
| `v=`, `v^=`, `v_=` | etiqueta de tensión |
| `i=`, `i^=`, `i_=` | etiqueta de corriente |
| `i>^=`, `i<^=` | corriente con flecha |
| `f=`, `f^=` | texto libre |
| `color=blue`, `thick`, `dashed` | estilo |

### Control fino de nodos visibles

`draw_nodes` controla los **puntos** y `label_nodes` controla las
**etiquetas de texto**. Casos de uso típicos:

| Querés mostrar | Combinación |
|---|---|
| Solo nodos principales (`1`, `2`) — default | `draw_nodes=primary, label_nodes=primary` |
| **Solo nodos específicos** que listés vos | `label_nodes={1, 2, out}` |
| Nodos nombrados con letra (`in`, `out`, `aux`) y nada más | nombralos así + `label_nodes=alpha` |
| Puntos sí, texto no | `draw_nodes=primary, label_nodes=none` |
| Nada (esquemático limpio para presentación) | `draw_nodes=none, label_nodes=none` |
| Solo uniones reales (3 o más conexiones) | `draw_nodes=connections` |

Convención que se aprovecha:
- Nombres **numéricos sin sufijo** (`1`, `2`, `3`) → "primarios" → se muestran con `primary`.
- Nombres con guión bajo (`0_1`, `2_aux`) → secundarios → quedan ocultos con `primary`.
- Nombres que **empiezan con letra** (`in`, `out`, `aux`) → reconocibles con `alpha`.

Truco para circuitos curriculares: usar `in` y `out` para los puertos
relevantes y nodos `2_aux`, `0_1`, etc. para layout interno. Con
`label_nodes=alpha` aparecen solo `in` y `out`.

### Opciones globales (línea que empieza con `;`)

```
; draw_nodes=connections, label_nodes=primary, label_ids=False, scale=0.8
```

| Opción | Valores | Default |
|---|---|---|
| `draw_nodes` | `all` / `none` / `primary` / `connections` | `primary` |
| `label_nodes` | `all` / `none` / `primary` / `alpha` / **`{n1, n2, ...}`** | `none` |
| `label_ids` | `True`/`False` | `True` |
| `label_values` | `True`/`False` | `True` |
| `style` | `american`/`british`/`european` | `american` |
| `voltage_dir` | `RP` (pasiva) / `EF` (activa) | `RP` |
| `scale` | float | `1.0` |
| `node_spacing` | float | `2.0` |

## Labels con comas internas (importante)

Labels que contengan secuencias LaTeX con coma como `\,` (espacio fino),
`\;`, `\:`, `\!` o coma decimal `{,}` se preservan sin necesidad de
envolver en llaves. Los siguientes funcionan tal cual:

```
V1 1 0; down, l=5\,I_1                  # ← 5 [espacio fino] I_1
R2 4 0; down, l=16{,}2\,V_a             # ← 16,2 V_a (coma decimal española)
F1 3 0 V1; up, l=r_m\,I_1
V3 1 0; down, l=0{,}0395\,V_1
```

Si encontrás un PDF generado de menos de ~2 KB y `to_pdf()` emite un
warning de "PDF sospechosamente chico", el problema suele ser una
label mal escapada — revisar las secuencias LaTeX y los espacios finos.

## Patrones que funcionan (importantísimo)

El motor de layout es **estricto con la consistencia direccional**. Si dos
componentes implican que un nodo debe estar simultáneamente a izquierda y
derecha de otro, lanza `RuntimeError: horizontal graph has a loop`.

**Patrón canónico para cerrar mallas**: usar **sub-nodos** (`0_1`, `0_2`)
en lugar de un único nodo de tierra, y wires explícitos entre ellos.

✅ Bien:
```
V1 1 0_1; down
R1 1 2; right=2
R2 2 0_2; down
W 0_1 0_2; right=2
```

❌ Mal (loop):
```
V1 1 0; down
R1 1 2; right
R2 2 0; down       # 0 aparece a la derecha (vía R1/R2) y a la izquierda (vía V1)
```

## Few-shot: descripción → netlist

### "Una resistencia R con un capacitor C en serie alimentados por una fuente AC"

```
V1 1 0_1 ac; down
R1 1 2; right
C1 2 0_2; down
W 0_1 0_2; right
; draw_nodes=connections
```

### "Un divisor de tensión 10 V con R1=1k y R2=2k"

```
V1 1 0_1 10; down
R1 1 2 1k; right=2.5
R2 2 0_2 2k; down=2
W 0_1 0_2; right=2.5
; draw_nodes=connections, label_nodes=primary
```

### "Un cuadripolo en T con impedancias genéricas Z_a, Z_b, Z_c"

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

### "Op-amp inversor con R1 a la entrada y R2 en realimentación"

```
P1 1 0_1; down
R1 1 2; right
R2 2_1 3_1; right
E1 3_2 0_3 opamp 2_0 2 A; mirror
W 0_1 0; right
W 2_0 0; down
W 3_2 3; right
W 0 0_3; right
P2 3 0_3; down
W 2_1 2; down
W 3_1 3_2; down
; draw_nodes=connections
```

### "Cuadripolo como caja negra con etiqueta 'Red R'"

Cuando el usuario NO quiere mostrar la topología interna (solo la
abstracción del dos-puertos), usar `TP` en lugar de armar la red con
`Z` en T/π:

```
TP1 1 2 3 4; right, l=Red\ R
W 1 1a; right=0.5, i^<=I_2
W 2 2a; right=0.5, i_=I_2
W 3a 3; right=0.5, i=I_1
W 4a 4; right=0.5, ir=I_1
P 1a 2a; down, v^=V_2
P 3a 4a; down, v_=V_1
; draw_nodes=none, label_nodes=none
```

Variantes:
- Para etiquetar con tipo de parámetros (Z, Y, H, ABCD, …): usar `TPZ`,
  `TPY`, `TPH`, `TPA`, `TPB`, `TPG` — la etiqueta sale automáticamente
  como TP_Z, TP_Y, etc.
- Para dibujar como **nube** en lugar de rectángulo (red indefinida):
  agregar `shape=cloud` a las opciones.

### "RLC paralelo alimentado por fuente de corriente AC"

```
I1 0_1 1 ac; up
W 1 2; right
R 2 0_2; down
W 2 3; right
L 3 0_3; down
W 3 4; right
C 4 0_4; down
W 0_1 0_2; right
W 0_2 0_3; right
W 0_3 0_4; right
; draw_nodes=connections
```

## Workflow recomendado

1. **Si el usuario pide algo conocido** (RC, RLC, divisor, etc.), buscá si
   tenés un template en [templates/](templates/) y adaptalo.
2. **Si pide algo nuevo**, generá el netlist primero y validalo con
   `n2t lint /tmp/nombre.sch` antes de renderizar.
3. **Si el render falla con loop**, leé el mensaje de error (incluye los
   componentes culpables) y corregí usando sub-nodos.
4. **Si el usuario pide cambios**, modificá el netlist existente —
   no regeneres todo desde cero.

## Templates disponibles

En [templates/](templates/) hay 19 netlists curriculares listos para usar
y adaptar:

| Tema | Templates |
|---|---|
| Pasivos básicos | `01_resistor_simple.sch`, `02_divisor_resistivo.sch` |
| Transitorios | `03_rc_transitorio.sch`, `05_rl_con_switch.sch` |
| Régimen senoidal | `04_rlc_serie.sch`, `11_resonante_paralelo.sch` |
| Impedancias | `09_impedancia_generica.sch`, `10_dipolo_thevenin.sch` |
| Cuadripolos | `06_cuadripolo.sch`, `17_cuadripolo_T.sch`, `18_cuadripolo_pi.sch`, `22_cuadripolo_caja_negra.sch` |
| Transformadores | `07_transformador.sch`, `21_transformador_real.sch` |
| Op-amps | `08_opamp_inversor.sch`, `14_opamp_no_inversor.sch`, `15_opamp_integrador.sch`, `16_opamp_derivador.sch` |
| Filtros | `19_filtro_RC_pasabajo.sch`, `20_filtro_CR_pasaalto.sch` |

## Documentación de referencia

Si necesitás detalles que no están en este cheatsheet:

- [REFERENCIA.md](REFERENCIA.md) — catálogo exhaustivo de componentes,
  opciones por componente, opciones globales, formatos de salida y
  errores típicos.
- [EJEMPLOS.md](EJEMPLOS.md) — galería visual con netlists comentados.

Leelos solo cuando hagan falta (no consumas contexto de entrada con la
referencia completa si la pregunta es simple).

## Salidas

Por defecto generá **PDF + PNG** en una carpeta sensata
(`/tmp/<nombre>.{pdf,png}` está bien si no hay ruta especificada).
El PNG sirve para mostrar inline; el PDF para integrar en LaTeX.

Si el usuario quiere el código TikZ para insertar en sus apuntes:
```bash
n2t render circuito.sch --tikz --no-standalone > circuito_frag.tex
```
