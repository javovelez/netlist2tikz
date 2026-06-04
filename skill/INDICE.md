# INDICE — despacho de búsqueda de la skill

**Punto de entrada de búsqueda.** Ante cualquier tarea que no esté en el cheatsheet
de `SKILL.md`, la skill busca **acá primero** y salta al id correspondiente.

```
rg -i "<palabra>" skill/INDICE.md     # 1) ubicar el id (cpt-… / param-… / gl-…)
rg "id: <id>" skill/COMPONENTES.md skill/PARAMETROS.md   # 2) leer la ficha
rg -l "n2t-tags:.*<tag>" skill/galeria/sch/              # 3) ejemplo real
```

- `cpt-*` → ficha en [COMPONENTES.md](COMPONENTES.md)
- `param-*` / `gl-*` → ficha en [PARAMETROS.md](PARAMETROS.md)
- temas y ejemplos → [galeria/](galeria/README.md) (índice máquina: `galeria/index.tsv`)

---

## Intención → dónde mirar

### Componentes / qué dibujar

| busco… (sinónimos) | ir a |
|---|---|
| resistencia, resistor | `cpt-r` |
| impedancia genérica, caja de impedancia, Z rectángulo | `cpt-z` (¡no `R` europea!) |
| admitancia, Y | `cpt-y` |
| inductancia, bobina, inductor, choke | `cpt-l` |
| capacitor, capacidad, condensador, electrolítico | `cpt-c` |
| elemento de fase constante, CPE | `cpt-cpe` |
| cable, wire, conexión, alambre | `cpt-w` |
| circuito abierto, gap | `cpt-o` |
| puerto, bornes, terminales | `cpt-p` |
| fuente de tensión, DC, continua, pila | `cpt-v` (forma DC) |
| fuente senoidal, alterna, AC, sinusoidal | `cpt-v` formas `ac` / `sin` |
| fuente escalón, step, u(t) | `cpt-v` forma `step` o `{...*u(t)}` |
| fuente de corriente | `cpt-i` |
| batería | `cpt-bat` |
| VCVS, fuente de tensión controlada por tensión | `cpt-e` |
| CCCS, controlada por corriente (corriente) | `cpt-f` |
| VCCS, transconductancia, gm | `cpt-g` |
| CCVS, transimpedancia | `cpt-h` |
| girador, gyrator | `cpt-gy` |
| opamp, amplificador operacional, inversor, no inversor | `cpt-opamp` · ej tema `05_opamps` |
| opamp diferencial / instrumentación | `cpt-opamp` (`fdopamp` / `inamp`) |
| transformador, trafo, relación de vueltas | `cpt-tf` |
| transformador con núcleo | `cpt-tf` (`TFcore` / `core=true`) |
| acoplamiento mutuo, inductancia mutua, k | `cpt-k` |
| cuadripolo, dos puertos, caja negra, red R | `cpt-tp` |
| cuadripolo con parámetros Z/Y/H/ABCD | `cpt-tpparam` |
| línea de transmisión, transmission line | `cpt-tl` |
| diodo, LED, zener, schottky, varicap | `cpt-d` (+ `kind=`) |
| transistor bipolar, BJT, npn, pnp | `cpt-q` |
| MOSFET, nmos, pmos, fet | `cpt-m` |
| JFET | `cpt-j` |
| válvula, triodo | `cpt-tv` |
| llave, switch, interruptor, pulsador, SPDT | `cpt-sw` |
| amperímetro, voltímetro, medidor | `cpt-meter` |
| chip, IC, MCU, compuerta lógica, flip-flop, mux | `cpt-u` |
| caja, círculo, triángulo (forma con texto) | `cpt-s` |
| bloque funcional, filtro como bloque, VCO | `cpt-bl` |
| mezclador, mixer | `cpt-mx` |
| punto suma, sumador, nodo suma | `cpt-sp` |
| función de transferencia, H(s) en caja | `cpt-tr` |
| anotación, texto suelto en un nodo | `cpt-a` |
| antena | `cpt-ant` |
| cristal, oscilador a cristal | `cpt-xt` |
| potenciómetro | `cpt-rv` |
| termistor, memristor, fusible, motor | `cpt-misc` |
| resorte, masa, amortiguador (mecánico) | `cpt-mec` |

### Cómo modificarlo / parámetros

| busco… (sinónimos) | ir a |
|---|---|
| orientar, dirección, hacia arriba/abajo/izq/der, largo | `param-dir` |
| estirar la rama, separar nodos | `param-size` · `gl-node_spacing` |
| wire escalonado, en L, con quiebre | `param-steps` · `param-free` |
| rotar, ángulo | `param-rotate` |
| escalar el símbolo / todo el dibujo | `param-scale` / `gl-scale` |
| espejar, invertir, voltear opamp/transistor | `param-mirror` · `param-flip` · `param-mirrorinputs` |
| poner en paralelo, desplazar al costado | `param-offset` |
| etiqueta, nombre, rótulo del componente | `param-l` |
| segunda etiqueta, anotación, valor aparte | `param-a` · `gl-annotate_values` |
| etiqueta de tensión, V con flecha, polaridad | `param-v` · `gl-voltage_dir` |
| etiqueta de corriente, flecha de corriente, I | `param-i` |
| etiqueta de flujo, potencia, sentido genérico | `param-f` |
| color, pintar, relleno | `param-color` · `param-fill` |
| línea gruesa, punteada, dashed | `param-line` |
| variante del símbolo (kind), tipo de diodo/cap/mosfet | `param-kind` |
| poner a tierra, masa, GND, referencia | `param-ground` · `gl-autoground` |
| riel de alimentación, Vcc, Vdd, Vss, Vee, 24V | `param-supply` |
| pin de entrada/salida, señal, pad | `param-pad` |
| atributo de un pin específico (.p .n .+ .-) | `param-dot` |
| etiquetas de pines de un chip | `param-pins` |
| flecha en un cable | `param-arrows` |
| coma decimal en la etiqueta, espacio fino, `\,` | `lbl-comas` |

### Opciones globales (línea `;`)

| busco… (sinónimos) | ir a |
|---|---|
| qué nodos se ven como punto | `gl-draw_nodes` |
| qué nodos llevan texto, ocultar nombres de nodos | `gl-label_nodes` |
| esquemático limpio / pelado (sin nodos ni labels) | `gl-draw_nodes`=none + `gl-label_nodes`=none |
| ocultar nombres (R1) / valores (1k) | `gl-label_ids` / `gl-label_values` |
| disposición del label (apilado, partido, solo nombre) | `gl-label_style` |
| formato del valor (eng) / problema con sci | `gl-label_value_style` (⚠️ solo `eng`) |
| estilo europeo / británico / americano | `gl-style` |
| convención de polaridad (pasiva/activa, RP/EF) | `gl-voltage_dir` |
| escala global, separación, tamaño base | `gl-scale` · `gl-node_spacing` · `gl-cpt_size` |
| grilla de depuración, ver el layout | `gl-help_lines` |
| tierra automática en los `0` | `gl-autoground` |
| resolución del PNG, dpi | `gl-dpi` |

### Problemas y recetas

| situación | qué hacer |
|---|---|
| **error `horizontal schematic graph has a loop`** | usar sub-nodos `0_1`,`0_2` + `W` de cierre. Patrón en `SKILL.md` §patrones. Ejemplos: `groundloop1-break` (tema 20) |
| PDF sospechosamente chico (<2 KB) | label mal escapada → `lbl-comas` |
| necesito el TikZ para Overleaf / mis apuntes | `n2t render x.sch --tikz [--no-standalone]` (ver `SKILL.md`) |
| quiero un circuito parecido a X | `rg -l "n2t-tags:.*X" skill/galeria/sch/` y adaptar el `.sch` |
| valor con unidades (Ω, kV) en la etiqueta | `l={50\,$\Omega$}` → `lbl-comas` |

### Conceptos curriculares (TCII / Señales)

Estos no son tags auto-derivados (no salen de los componentes); buscá por nombre/tema.

| concepto (sinónimos) | dónde |
|---|---|
| divisor de tensión | `galeria/sch/00_curricular/02_divisor_resistivo.sch` · `rg -li "voltage-divider" galeria/sch/` |
| RC / RL transitorio, carga/descarga, escalón | `rg -li "rc_transitorio|rl_con_switch" galeria/sch/00_curricular/` · tema `11_switches` |
| RLC serie/paralelo, resonancia, régimen senoidal | `rg -li "rlc|resonante" galeria/sch/00_curricular/` · `cpt-v` forma `ac` |
| dipolo Thévenin / Norton | `rg -li "thevenin|dipolo" galeria/sch/00_curricular/` |
| cuadripolo T / π / caja negra | `galeria/sch/00_curricular/` (`17_cuadripolo_T`, `18_cuadripolo_pi`, `22_cuadripolo_caja_negra`) · `cpt-tp` |
| transformador real / con fugas | `galeria/sch/00_curricular/21_transformador_real.sch` · `cpt-tf` |
| opamp inversor / no inversor / integrador / derivador | `rg -li "opamp|integrador|derivador" galeria/sch/00_curricular/` · tema `05_opamps` |
| filtro pasa-bajo / pasa-alto | `rg -li "filtro|lpf|sallen" galeria/sch/` · `kind:lowpass` `kind:highpass` |
| fuente controlada (VCCS/CCCS/…) | `galeria/sch/00_curricular/` (`12_fuente_VCCS`, `13_fuente_CCCS`) · `cpt-g` `cpt-f` |

---

## Vocabulario de tags (controlado)

Tags válidos para `rg -l "n2t-tags:.*<tag>" skill/galeria/sch/`. Combinables.

- **Tema**: `pasivo` `fuente` `diodo` `transistor` `opamp` `magnetico` `cuadripolo`
  `red` `analisis` `simplificacion` `switch` `logica` `bloque` `diagrama-bloques`
  `dsp` `chip` `cmos` `linea-transmision` `medidor` `tierra` `etiqueta` `intro` `varios`
- **Componente**: `cpt:r` `cpt:l` `cpt:c` `cpt:z` `cpt:y` `cpt:v` `cpt:i` `cpt:e`
  `cpt:f` `cpt:g` `cpt:h` `cpt:tf` `cpt:k` `cpt:tp` `cpt:d` `cpt:q` `cpt:m` `cpt:j`
  `cpt:sw` `cpt:w` `cpt:o` `cpt:p` `cpt:u` `cpt:bl` `cpt:gy` `cpt:cpe` `cpt:fb`
  `cpt:xt` `cpt:rv` `cpt:bat` `cpt:am` `cpt:vm` `cpt:ant` `cpt:tl` `cpt:mx` `cpt:sp`
  `cpt:tr` `cpt:shape` `cpt:mecanico` `cpt:rel` `cpt:misc`
- **Feature/parámetro**: `etiqueta` `etiqueta-v` `etiqueta-i` `etiqueta-f` `anotacion`
  `espejo` `rotacion` `estilo` `estilo-simbolo` `kind` `forma` `imagen` `layout`
  `tierra` `alimentacion` `pad-senal` `etiqueta-nodo` `nodo-pin` `pines`
  `visibilidad-nodos` `etiquetas-globales` `geometria-global` `grilla` `convencion`
  `control` `raw-tikz`
- **kind:** `kind:schottky` `kind:led` `kind:zener` `kind:electrolytic` `kind:polar`
  `kind:nmos` `kind:pmos` `kind:nfet` `kind:choke` `kind:lowpass` `kind:highpass`
  `kind:vco` `kind:coax` `kind:cell1` `kind:tx` `kind:rx` … (ver `galeria/index.tsv`)
- **Curricular**: `curricular:tcii` · `curricular:senales`

---

## Ruta curricular

**Teoría de Circuitos II** — pasivos, fuentes, régimen senoidal/resonancia,
transitorios, cuadripolos, transformadores, opamps, filtros:
[01_pasivos](galeria/01_pasivos.md) · [02_fuentes](galeria/02_fuentes.md) ·
[05_opamps](galeria/05_opamps.md) · [06_magneticos](galeria/06_magneticos.md) ·
[07_cuadripolos](galeria/07_cuadripolos.md) · [08_redes](galeria/08_redes.md) ·
[09_analisis](galeria/09_analisis.md) · [10_simplificacion](galeria/10_simplificacion.md) ·
[11_switches](galeria/11_switches.md) · [19_medidores](galeria/19_medidores.md) ·
[20_tierras_alimentacion](galeria/20_tierras_alimentacion.md) ·
[21_etiquetas](galeria/21_etiquetas.md) · [22_intro](galeria/22_intro.md)

**Análisis de Señales y Sistemas** — diagramas de bloques, FIR/tiempo discreto,
lógica, bloques funcionales:
[12_logica](galeria/12_logica.md) · [13_formas_bloques](galeria/13_formas_bloques.md) ·
[14_diagramas_bloques](galeria/14_diagramas_bloques.md) · [15_dsp_fir](galeria/15_dsp_fir.md)

---

## Mapa de archivos

| archivo | qué tiene |
|---|---|
| [SKILL.md](SKILL.md) | entry point: cheatsheet 90%, protocolo de búsqueda, convenciones |
| [INDICE.md](INDICE.md) | este despacho: intención→id, tags, ruta curricular |
| [COMPONENTES.md](COMPONENTES.md) | ficha por componente (`cpt-*`) |
| [PARAMETROS.md](PARAMETROS.md) | ficha por parámetro (`param-*`, `gl-*`) |
| [galeria/README.md](galeria/README.md) | galería: 23 temas, ~500 ejemplos, índice máquina |
| [galeria/index.tsv](galeria/index.tsv) | índice máquina (id·tema·archivo·título·tags·cpts·params) |
| [galeria/RENDER_REPORT.md](galeria/RENDER_REPORT.md) | qué reproduce el fork (497/500) |
