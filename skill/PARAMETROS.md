# PARAMETROS — registro unificado de cada parámetro modificable

Catálogo de **todos** los parámetros que se pueden poner después del `;` en una
línea de componente, o en la línea global (la que empieza con `;`). Cada parámetro
tiene una **ficha de campos fijos** con un `id:` estable para grep.

> **Cómo busca la skill aquí**
> 1. Por id exacto: `rg "id: param-i" skill/PARAMETROS.md` → leé las ~8 líneas siguientes.
> 2. Por concepto: `rg -i "corriente|flecha" skill/PARAMETROS.md`.
> 3. Si no sabés el nombre, mirá primero `skill/INDICE.md` (intención → id).

**Legenda**
`ámbito`: **componente** (va en la línea del componente) · **global** (línea `;`) ·
**nodo** (atributo de un nodo). `fork`: **✅** verificado que renderiza · **⚠️** funciona
con salvedad · **❌** no soportado por el fork. Las variantes de etiqueta llevan
modificadores `^`/`_` (arriba/abajo) y `<`/`>` (sentido).

---

## Índice rápido (1 línea por parámetro)

| parámetro | id | ámbito | grupo | qué hace | fork |
|---|---|---|---|---|---|
| `right` `left` `up` `down` `=N` | `param-dir` | componente | dirección | orienta y fija el largo | ✅ |
| `size` | `param-size` | componente | dirección | estira la separación entre nodos | ✅ |
| `free` | `param-free` | componente | dirección | nodos sin restricción (wires escalonados) | ✅ |
| `fixed` | `param-fixed` | componente | dirección | no estirar | ✅ |
| `rotate=θ` | `param-rotate` | componente | geometría | rota θ grados antihorario | ✅ |
| `scale` | `param-scale` | componente | geometría | escala el símbolo | ✅ |
| `offset` | `param-offset` | componente | geometría | desplaza ⊥ a la rama (paralelos) | ✅ |
| `mirror` | `param-mirror` | componente | espejo | espeja en el eje de la rama | ✅ |
| `invert` | `param-invert` | componente | espejo | invierte vertical | ✅ |
| `fliplr` `flipud` | `param-flip` | componente | espejo | voltea horizontal / vertical | ✅ |
| `mirrorinputs` | `param-mirrorinputs` | componente | espejo | intercambia entradas de opamp | ✅ |
| `aspect` `width` | `param-aspect` | componente | geometría | relación/ancho de cajas | ✅ |
| `l` `l^` `l_` | `param-l` | componente | etiqueta | etiqueta del componente | ✅ |
| `a` `a^` `a_` | `param-a` | componente | etiqueta | anotación (segunda etiqueta) | ✅ |
| `t` | `param-t` | componente | etiqueta | etiqueta interna (formas) | ✅ |
| `v` `v^` `v_` `v<` `v>` | `param-v` | componente | tensión | etiqueta de tensión | ✅ |
| `i` … `ir` | `param-i` | componente | corriente | etiqueta/flecha de corriente | ✅ |
| `f` … | `param-f` | componente | flujo | etiqueta de flujo | ✅ |
| `color` | `param-color` | componente | estilo | color (xcolor) | ✅ |
| `fill` | `param-fill` | componente | estilo | relleno de formas cerradas | ✅ |
| `thick` `dashed` `dotted` | `param-line` | componente | estilo | estilo de línea (TikZ) | ✅ |
| `kind` | `param-kind` | componente | tipo | variante del símbolo | ✅ |
| `variable` | `param-variable` | componente | tipo | R/L/C variable | ✅ |
| `core` | `param-core` | componente | tipo | núcleo en transformador | ✅ |
| `shape` | `param-shape` | componente | tipo | forma de cuadripolo/bloque | ✅ |
| `image` | `param-image` | componente | tipo | reemplaza símbolo por imagen | ⚠️ |
| `nosim` `nodraw` `invisible` `ignore` | `param-control` | componente | control | conectar/dibujar selectivo | ✅ |
| tierras (`ground` `sground` `0V` …) | `param-ground` | nodo | conexión | símbolo de tierra | ✅ |
| alimentación (`vdd` `vss` `vcc` `vee`) | `param-supply` | nodo | conexión | riel de alimentación | ✅ |
| señal (`input` `output` `bidir` `pad`) | `param-pad` | nodo | conexión | pin de señal | ✅ |
| sintaxis punto `.p.l` `.-.implicit` | `param-dot` | nodo | conexión | atributo por pin | ✅ |
| `pins` `pinlabels` `pindefs` `anchors` | `param-pins` | componente | chips | etiquetas de pines de IC | ✅ |
| `steps` | `param-steps` | componente | cable | wire escalonado | ✅ |
| `startarrow` `endarrow` | `param-arrows` | componente | cable | flechas en wire | ✅ |
| `nowires` | `param-nowires` | componente | cable | sin wires de tierra (líneas) | ✅ |
| coma decimal / `\,` en labels | `lbl-comas` | — | etiqueta | escape de comas en etiquetas | ✅ |
| **`draw_nodes`** | `gl-draw_nodes` | global | nodos | qué nodos se dibujan (punto) | ✅ |
| **`label_nodes`** | `gl-label_nodes` | global | nodos | qué nodos se etiquetan (texto) | ✅ |
| **`label_ids`** | `gl-label_ids` | global | etiquetas | mostrar nombres (R1, C1) | ✅ |
| **`label_values`** | `gl-label_values` | global | etiquetas | mostrar valores (1k) | ✅ |
| **`label_style`** | `gl-label_style` | global | etiquetas | disposición nombre/valor | ✅ |
| **`label_value_style`** | `gl-label_value_style` | global | etiquetas | formato de valor (solo `eng`) | ⚠️ |
| **`label_flip`** | `gl-label_flip` | global | etiquetas | invierte lado del label | ✅ |
| **`annotate_values`** | `gl-annotate_values` | global | etiquetas | valor como anotación aparte | ✅ |
| **`style`** | `gl-style` | global | símbolos | american / british / european | ✅ |
| **`voltage_dir`** | `gl-voltage_dir` | global | convención | RP (pasiva) / EF (activa) | ✅ |
| **`scale`** | `gl-scale` | global | geometría | escala global | ✅ |
| **`cpt_size`** | `gl-cpt_size` | global | geometría | largo base de componentes | ✅ |
| **`node_spacing`** | `gl-node_spacing` | global | geometría | separación base entre nodos | ✅ |
| **`help_lines`** | `gl-help_lines` | global | depuración | grilla de ayuda | ✅ |
| **`autoground`** | `gl-autoground` | global | conexión | tierra automática en nodos `0` | ✅ |
| **`anchor`** | `gl-anchor` | global | layout | anclaje del bounding box | ✅ |
| **`dpi`** | `gl-dpi` | global | salida | resolución del PNG | ✅ |

---

## Dirección y largo

### `right` `left` `up` `down` (y `=N`) — dirección y largo
`id: param-dir` · ámbito: componente · grupo: dirección · fork: ✅
- **valores** `right`=0°, `left`=180°, `up`=90°, `down`=−90°. Forma `=N` agrega largo (factor de separación; con `node_spacing=2`, `right=2` ≈ 2 unidades).
- **default** la dirección es **respecto del primer nodo**; sin dirección, horizontal.
- **qué hace** orienta el componente y, con `=N`, fija el largo de la rama.
- **ejemplo** `R1 1 2; right=2` · `C1 2 0_2; down=1.5`
- **gotcha** el placer **exige consistencia direccional**: si dos componentes piden que un nodo esté a izquierda y derecha a la vez → `RuntimeError: ... loop`. Solución: sub-nodos (`0_1`, `0_2`) + wires explícitos. Ver `g-loop` en INDICE.
- **ver** `param-size` · `param-free`

### `size` — estira la separación entre nodos
`id: param-size` · ámbito: componente · grupo: dirección · fork: ✅
- **valores** float (factor) · **default** 1
- **qué hace** escala la **distancia entre los nodos** del componente sin cambiar la dirección (estira la rama; el símbolo queda igual). Distinto de `scale` (que agranda el símbolo).
- **ejemplo** `C1 2 3; right, size=1.5`
- **ver** `param-scale` · `gl-node_spacing`

### `free` — nodos sin restricción
`id: param-free` · ámbito: componente · grupo: dirección · fork: ✅
- **qué hace** no impone restricciones de posición a los nodos; útil para **wires escalonados**. Con `free` se ignoran `size` y `rotate`.
- **ejemplo** `W 1 2; free` · **ver** `param-steps`

### `fixed` — no estirar
`id: param-fixed` · ámbito: componente · grupo: dirección · fork: ✅
- **qué hace** evita que el componente se estire para satisfacer el layout.
- **ejemplo** `R1 1 2; right, fixed`

---

## Geometría y orientación

### `rotate=θ` — rotación arbitraria
`id: param-rotate` · ámbito: componente · grupo: geometría · fork: ✅
- **valores** ángulo en grados, antihorario (0° = +x) · **ejemplo** `D1 1 2; right, rotate=45`
- **gotcha** se ignora si está `free`.

### `scale` — escala el símbolo
`id: param-scale` · ámbito: componente · grupo: geometría · fork: ✅
- **qué hace** factor de escala del **largo del símbolo** (no de la rama). Para escalar todo el dibujo usá el global `gl-scale`.
- **ejemplo** `Q1 c b e; up, scale=1.5` · **ver** `param-size` · `gl-scale`

### `offset` — desplazamiento perpendicular
`id: param-offset` · ámbito: componente · grupo: geometría · fork: ✅
- **qué hace** desplaza el componente ⊥ a su rama; útil para **componentes en paralelo**.
- **ejemplo** `R2 1 2; right, offset=0.5`

### `mirror` — espejo en el eje de la rama
`id: param-mirror` · ámbito: componente · grupo: espejo · fork: ✅
- **qué hace** espeja (en x) el componente; típico en **opamps y transistores** para invertir entradas. **ejemplo** `E1 3 0 opamp 1 2 A; right, mirror`
- **ver** `param-mirrorinputs` · `param-invert`

### `invert` — invierte vertical
`id: param-invert` · ámbito: componente · grupo: espejo · fork: ✅
- **qué hace** invierte el componente verticalmente. **ejemplo** `D1 1 2; up, invert`

### `fliplr` `flipud` — voltear
`id: param-flip` · ámbito: componente · grupo: espejo · fork: ✅
- **qué hace** `fliplr` voltea izquierda↔derecha; `flipud` arriba↔abajo. **ejemplo** `M1 d g s; up, fliplr`

### `mirrorinputs` — intercambia entradas de opamp
`id: param-mirrorinputs` · ámbito: componente · grupo: espejo · fork: ✅
- **qué hace** intercambia `+`/`−` del opamp **sin** espejar todo el cuerpo. **ejemplo** `E1 3 0 opamp 1 2 A; right, mirrorinputs`
- **ver** `param-mirror`

### `aspect` `width` — proporción/ancho de cajas
`id: param-aspect` · ámbito: componente · grupo: geometría · fork: ✅
- **qué hace** `aspect`=relación de aspecto de cajas/formas; `width`=ancho del componente. **ejemplo** `TP1 1 2 3 4; right, aspect=1.4`

---

## Etiquetas principales

### `l` `l^` `l_` — etiqueta del componente
`id: param-l` · ámbito: componente · grupo: etiqueta · fork: ✅
- **valores** texto o LaTeX (`$...$` o directo) · **default** nombre+valor (p.ej. `R1=1k`)
- **posición** `l^` arriba · `l_` abajo · `l` automática (también `l<`/`l>` izq/der en horizontal)
- **qué hace** reemplaza la etiqueta automática por una propia. **Convención del autor**: para impedancia genérica usá el componente `Z` con `l=Z_1` (no `R` europea).
- **ejemplo** `Z1 1 2; right, l=Z_a` · `R2 3 0; down, l^=10k`
- **gotcha** comas/`\,` en la etiqueta → ver `lbl-comas`. **ver** `param-a` · `gl-label_ids`

### `a` `a^` `a_` — anotación (segunda etiqueta)
`id: param-a` · ámbito: componente · grupo: etiqueta · fork: ✅
- **qué hace** agrega una **segunda** etiqueta junto al componente (p.ej. el valor además del nombre). **ejemplo** `R1 1 2; right, l=R_1, a=1k`
- **ver** `gl-annotate_values`

### `t` — etiqueta interna
`id: param-t` · ámbito: componente · grupo: etiqueta · fork: ✅
- **qué hace** texto **dentro** de la forma (cajas, cuadripolos, chips). **ejemplo** `TP1 1 2 3 4; right, t=Red`

---

## Tensión

### `v` `v^` `v_` `v<` `v>` — etiqueta de tensión
`id: param-v` · ámbito: componente · grupo: tensión · fork: ✅
- **valores** texto/LaTeX · **default** — (sin etiqueta)
- **variantes** `v^` (arriba) · `v_` (abajo) · `v<` `v>` (sentido de la flecha) · combinaciones `v^>` `v^<` `v_>` `v_<`
- **posición/sentido** `^`/`_` ubican arriba/abajo; `<`/`>` fijan el sentido de la flecha de referencia. El sentido depende además del global `voltage_dir` (RP vs EF).
- **qué hace** dibuja la flecha/etiqueta de tensión sobre el componente.
- **ejemplo** `R1 1 2; right, v^=V_{R_1}` · `R2 3 0; down, v<=V_{R_2}`
- **ver** `param-i` · `gl-voltage_dir` · `lbl-comas`

---

## Corriente

### `i` (+ variantes) — etiqueta/flecha de corriente
`id: param-i` · ámbito: componente · grupo: corriente · fork: ✅
- **valores** texto/LaTeX · **default** — (sin etiqueta). Vacía (`i>=`) = solo flecha.
- **variantes** `i^` `i_` · `i<` `i>` · `i>^` `i<^` `i>_` `i<_` `i^>` `i^<` `i_>` `i_<` · `ir`
- **posición** `<`/`>` fijan el sentido; si el `<`/`>` va **antes** de `^`/`_`, la etiqueta queda al **inicio** del componente, si no, al **final**.
- **qué hace** dibuja flecha y/o etiqueta de corriente.
- **ejemplo** `R1 1 2; right, i>^=I_1` · `L 2 3; right, i>^=I_L`
- **gotcha** coma decimal / `\,` → `lbl-comas`. **ver** `param-v` · `param-f`

---

## Flujo

### `f` (+ variantes) — etiqueta de flujo
`id: param-f` · ámbito: componente · grupo: flujo · fork: ✅
- **variantes** mismas que corriente: `f^` `f_` `f<` `f>` `f>^` `f<^` `f>_` `f<_` `f^>` `f^<` `f_>` `f_<`
- **posición** igual regla que `param-i` (`<`/`>` antes de `^`/`_` → inicio).
- **qué hace** etiqueta de **flujo** (potencia/energía/genérica) sin la convención eléctrica de la corriente. Útil para "primario", "carga", flujo de señal.
- **ejemplo** `W 1 2; right, f>^=P_{in}`
- **ver** `param-i`

---

## Estilo visual

### `color` — color del componente
`id: param-color` · ámbito: componente · grupo: estilo · fork: ✅
- **valores** cualquier color de `xcolor` (`blue`, `red!60!black`, …) · **ejemplo** `R1 1 2; right=2, color=blue`

### `fill` — relleno
`id: param-fill` · ámbito: componente · grupo: estilo · fork: ✅
- **qué hace** rellena formas cerradas (cajas, cuadripolos, bloques). **ejemplo** `TP1 1 2 3 4; right, fill=blue!15`

### `thick` `dashed` `dotted` — estilo de línea
`id: param-line` · ámbito: componente · grupo: estilo · fork: ✅
- **qué hace** estilos de línea de TikZ que pasan directo (`thick`, `ultra thick`, `dashed`, `dotted`, `line width=...`). **ejemplo** `W 1 2; right, dashed`
- **gotcha** son estilos de circuitikz/TikZ; cualquier estilo válido de TikZ pasa.

---

## Tipo / variante

### `kind` — variante del símbolo
`id: param-kind` · ámbito: componente · grupo: tipo · fork: ✅
- **qué hace** selecciona la **variante de dibujo** del componente. Los valores dependen del componente (ver `COMPONENTES.md`):
  - **C**: `electrolytic` `polar` `variable` `curved` `sensor` `tunable`
  - **L**: `variable` `choke` `twolineschoke` `tunable` `sensor` `american` `european`
  - **D**: `schottky` `led` `zener` `zzener` `tunnel` `photo` `varcap` `bidirectional` `tvs` `laser`
  - **M (MOSFET)**: `nmos` `pmos` `nfet` `pfet` `nfetd` `pfetd` `nigfete` `pigfete` `hemt` …
  - **BL (bloque)**: `lowpass` `highpass` `bandpass` `amp` `vco` `adc` `dac` `dcdc` `phaseshifter` `fft` …
  - **MISC**: `thermistor` `memristor` · **BAT**: `cell1` · **ANT**: `tx` `rx`
- **ejemplo** `D1 1 2; right, kind=schottky` · `C1 1 0; down, kind=electrolytic`
- **ver** `param-variable` · `param-core`

### `variable` — R/L/C variable
`id: param-variable` · ámbito: componente · grupo: tipo · fork: ✅
- **qué hace** dibuja la flecha de "variable" sobre R/L/C. Equivale a `kind=variable`. **ejemplo** `R1 1 2; right, variable`

### `core` — núcleo de transformador
`id: param-core` · ámbito: componente · grupo: tipo · fork: ✅
- **qué hace** dibuja el núcleo (líneas entre espiras) del transformador. También como componente `TFcore`. **ejemplo** `TF 1 0 2 0; right, core=true` · **ver** `cpt-tf`

### `shape` — forma de cuadripolo / bloque
`id: param-shape` · ámbito: componente · grupo: tipo · fork: ✅
- **qué hace** cambia la forma del contenedor (p.ej. `cloud` para "red indefinida" en cuadripolos). **ejemplo** `TP1 1 2 3 4; right, shape=cloud`

### `image` — reemplaza símbolo por imagen
`id: param-image` · ámbito: componente · grupo: tipo · fork: ⚠️
- **qué hace** usa una imagen (PNG/PDF) en lugar del símbolo de una forma `S`. **⚠️** requiere que el archivo de imagen exista junto al `.tex`; si falta, el render falla.
- **ejemplo** `S1 box; right=4, image=cmos1.png`

---

## Control de dibujo

### `nosim` `nodraw` `invisible` `ignore` — conectar/dibujar selectivo
`id: param-control` · ámbito: componente · grupo: control · fork: ✅
- **`nosim`** se ignora para el esquemático (sólo afectaba al análisis; en este fork es inocuo).
- **`invisible`** conecta con los demás pero **no** se dibuja.
- **`nodraw`** conecta y genera la macro circuitikz pero sin el argumento `draw`.
- **`ignore`** ni conecta ni dibuja.
- **ejemplo** `W 1 2; right, invisible`

---

## Conexiones implícitas (tierras, alimentación, señal)

### tierras: `ground` `sground` `0V` … — símbolo de tierra
`id: param-ground` · ámbito: nodo · grupo: conexión · fork: ✅
- **valores** `ground` (tierra/earth) · `sground` (señal) · `cground` (chasis) · `nground` (sin ruido) · `pground` (protegida) · `rground` (referencia) · `tground` `tlground` (sin cola) · `eground` `eground2` (europea) · `0V` · `implicit` (default `sground`)
- **qué hace** dibuja el símbolo de tierra en el nodo (se pone como atributo de un `W` o nodo). **ejemplo** `W 1 0; down, sground` · `W 1 0; down, ground`
- **ver** `gl-autoground` (tierra automática en nodos `0`)

### alimentación: `vdd` `vss` `vcc` `vee` — riel de alimentación
`id: param-supply` · ámbito: nodo · grupo: conexión · fork: ✅
- **qué hace** dibuja el símbolo de riel: `vcc`/`vdd` (positivo, primer nodo), `vee`/`vss` (negativo, último nodo). **ejemplo** `W 1 2; right, vdd, l=24V`
- **ver** `param-dot`

### señal: `input` `output` `bidir` `pad` — pin de señal
`id: param-pad` · ámbito: nodo · grupo: conexión · fork: ✅
- **qué hace** dibuja un pin/pad de entrada, salida, bidireccional o pad. **ejemplo** `W 1 2; right=0.2, input, l=in, fill=blue!50`

### sintaxis punto: `.p.l` `.-.implicit` … — atributo por pin
`id: param-dot` · ámbito: nodo · grupo: conexión · fork: ✅
- **qué hace** aplica un atributo a un **pin específico** del componente con prefijo `.pin.attr`. Pines: bipolos `p`/`+`, `n`/`−`; BJT `c`/`b`/`e`; FET `d`/`g`/`s`; chips por nombre.
- **ejemplo** `R 1 2; down, .+.implicit, .+.l=24V, .-.implicit, .-.l=-24V` · `M1 d g s; up, .s.vss`

---

## Pines de chips / formas

### `pins` `pinlabels` `pinnames` `pinnodes` `pindefs` `anchors` — pines de IC
`id: param-pins` · ámbito: componente · grupo: chips · fork: ✅
- **qué hace** define/etiqueta los pines de un chip o forma (`U...`, `S...`). `anchors` elige qué anclas mostrar. **ejemplo** `U1 chip2121; right=2, l=MCU, pinlabels={l1=SDA,l2=SCL}`
- **ver** `cpt-u`

---

## Cable (atributos de `W`)

### `steps` — wire escalonado
`id: param-steps` · ámbito: componente · grupo: cable · fork: ✅
- **qué hace** dibuja el wire con escalones: `-` tramo horizontal, `|` tramo vertical (numérico repite: `steps=-2|-`). Suele ir con `free`. **ejemplo** `W 1 2; free, steps=-|-`

### `startarrow` `endarrow` — flechas en wire
`id: param-arrows` · ámbito: componente · grupo: cable · fork: ✅
- **qué hace** pone una flecha al inicio/fin del wire (nombres de flecha TikZ: `tri`, `otri`, `stealth`, …). **ejemplo** `W 1 2; right, endarrow=tri`

### `nowires` — sin wires de tierra
`id: param-nowires` · ámbito: componente · grupo: cable · fork: ✅
- **qué hace** en líneas de transmisión, omite los wires de tierra. **ejemplo** `TL1 1 2 3 4; right=2, nowires`

---

## Etiquetas con comas / coma decimal

### coma decimal y `\,` en etiquetas
`id: lbl-comas` · ámbito: etiqueta · grupo: etiqueta · fork: ✅
- **qué hace** las secuencias LaTeX con coma (`\,` espacio fino, `\;`, `\:`, `\!`) y la **coma decimal española** `{,}` se preservan **sin** romper el parseo de opciones (parche del fork).
- **ejemplo** `V1 1 0; down, l=5\,I_1` · `R2 4 0; down, l=16{,}2\,V_a` · `V3 1 0; down, l=0{,}0395\,V_1`
- **gotcha** si un PDF sale < ~2 KB y `to_pdf()` avisa "PDF sospechosamente chico", suele ser una label mal escapada.

---

## GLOBALES (línea que empieza con `;`)

Se ponen en una línea sola con `;` al principio, o como kwargs a `draw()`/`to_pdf()`.
Fuente autoritativa: `netlist2tikz/rcdefaults.py`.

### `draw_nodes` — qué nodos se dibujan (punto)
`id: gl-draw_nodes` · ámbito: global · grupo: nodos · fork: ✅
- **valores** `all` · `none` · `primary` · `connections` · `labeled` · **default** `labeled` (default del fork; lcapy upstream usa `primary`)
- **qué hace** `labeled`=**solo terminales/puertos (open-circle) y nodos con etiqueta visible**; el resto (uniones internas) invisible. `primary`=nodos sin guión bajo inicial; `connections`=solo uniones (3+ ramas); `none`=ninguno; `all`=todos.
- **nota** `labeled` es el modo que deja los esquemáticos limpios por defecto: puntos solo donde hay puerto o etiqueta. Implementado en `schemnode.py:visible()` + `cpt.py:draw_node()`.
- **ejemplo** `; draw_nodes=connections` para volver al estilo "punto en cada unión" · **ver** `gl-label_nodes`

### `label_nodes` — qué nodos se etiquetan (texto)
`id: gl-label_nodes` · ámbito: global · grupo: nodos · fork: ✅
- **valores** `all` · `alpha` · `none` · `primary` · **default** **`none`** (default del fork; lcapy upstream usa `primary`)
- **qué hace** `none`=ninguno (figuras limpias, sin números de nodo); `primary`=nodos numéricos sin sufijo; `alpha`=solo los que empiezan con letra (`in`, `out`); `all`=todos (debug).
- **nota** con `draw_nodes=labeled` (default), poner una etiqueta visible (`label_nodes=all`/`primary` o etiqueta explícita) hace que ese nodo **también muestre el punto**.
- **ejemplo** `; label_nodes=alpha` · **ver** `gl-draw_nodes`

### `label_ids` — mostrar nombres
`id: gl-label_ids` · ámbito: global · grupo: etiquetas · fork: ✅
- **valores** `true`/`false` · **default** `true` · **qué hace** muestra/oculta los nombres (`R1`, `C1`). **ejemplo** `; label_ids=false`

### `label_values` — mostrar valores
`id: gl-label_values` · ámbito: global · grupo: etiquetas · fork: ✅
- **valores** `true`/`false` · **default** `true` · **qué hace** muestra/oculta los valores (`1k`, `100n`). **ejemplo** `; label_values=false`

### `label_style` — disposición nombre/valor
`id: gl-label_style` · ámbito: global · grupo: etiquetas · fork: ✅
- **valores** `aligned` · `stacked` · `split` · `value` · `name` · **default** `aligned`
- **qué hace** `aligned`=nombre=valor en una línea; `stacked`=nombre sobre valor; `split`=en lados opuestos; `name`=solo nombre; `value`=solo valor.
- **ejemplo** `; label_style=stacked`

### `label_value_style` — formato del valor
`id: gl-label_value_style` · ámbito: global · grupo: etiquetas · fork: ⚠️
- **valores** `eng[N]` (p.ej. `eng3`, `eng2`) · **default** `eng3`
- **⚠️ limitación del fork** solo la familia **`eng`**. `sci`, `spice`, `ratfun`, `sympy` → **error** `Unsupported style`. (El fork removió el formateo no-`eng`.)
- **ejemplo** `; label_value_style=eng2`

### `label_flip` — invierte lado del label
`id: gl-label_flip` · ámbito: global · grupo: etiquetas · fork: ✅
- **valores** `true`/`false` · **default** `false` · **ejemplo** `; label_flip=true`

### `annotate_values` — valor como anotación aparte
`id: gl-annotate_values` · ámbito: global · grupo: etiquetas · fork: ✅
- **valores** `true`/`false` · **default** `false` · **qué hace** pone el valor como anotación separada del nombre. **ejemplo** `; annotate_values=true`

### `style` — estilo de símbolos
`id: gl-style` · ámbito: global · grupo: símbolos · fork: ✅
- **valores** `american` · `british` · `european` · **default** `american`
- **qué hace** `american`=R zigzag, L espiral; `european`=R rectángulo IEC, L rectángulo. **Afecta a R/L, no a `Z`.** Convención del autor: dejar `american` y usar `Z` para impedancias rectangulares.
- **ejemplo** `; style=european`

### `voltage_dir` — convención de polaridad
`id: gl-voltage_dir` · ámbito: global · grupo: convención · fork: ✅
- **valores** `RP` (rising potential / referencia pasiva) · `EF` (electric field / activa) · **default** `RP`
- **ejemplo** `; voltage_dir=EF` · **ver** `param-v`

### `scale` — escala global
`id: gl-scale` · ámbito: global · grupo: geometría · fork: ✅
- **valores** float · **default** 1.0 · **ejemplo** `; scale=0.8` · **ver** `param-scale`

### `cpt_size` — largo base de componentes
`id: gl-cpt_size` · ámbito: global · grupo: geometría · fork: ✅
- **valores** float · **default** 1.5 · **ejemplo** `; cpt_size=1.2`

### `node_spacing` — separación base entre nodos
`id: gl-node_spacing` · ámbito: global · grupo: geometría · fork: ✅
- **valores** float · **default** 1.2 (default del fork, dibujos compactos; lcapy upstream usa 2.0) · **ejemplo** `; node_spacing=2.5` · **ver** `param-size`

### `help_lines` — grilla de ayuda
`id: gl-help_lines` · ámbito: global · grupo: depuración · fork: ✅
- **valores** float (espaciado; 0 = off) · **default** 0 · **qué hace** dibuja una grilla de referencia para depurar el layout. **ejemplo** `; help_lines=1`

### `autoground` — tierra automática
`id: gl-autoground` · ámbito: global · grupo: conexión · fork: ✅
- **valores** `none`/`false`/`true` o un tipo de tierra (`ground`, `sground`, …) · **default** `none`
- **qué hace** dibuja tierra automáticamente en los nodos `0`. **ejemplo** `; autoground=true` · **ver** `param-ground`

### `anchor` — anclaje del bounding box
`id: gl-anchor` · ámbito: global · grupo: layout · fork: ✅
- **valores** dirección cardinal (`south east`, `north`, …) · **default** `south east` · **ejemplo** `; anchor=north`

### `dpi` — resolución del PNG
`id: gl-dpi` · ámbito: global · grupo: salida · fork: ✅
- **valores** int · **default** 300 · **qué hace** resolución del PNG (kwarg de `to_png`/`--dpi`). **ejemplo** `n2t render x.sch -o x.png --dpi 600`
