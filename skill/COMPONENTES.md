# COMPONENTES — catálogo de cada componente del netlist

Cada componente entendido por `netlist2tikz` (gramática completa de lcapy,
conservada por el fork) con su **ficha de campos fijos** e `id:` estable.

> **Cómo busca la skill aquí**
> 1. Por id: `rg "id: cpt-tf" skill/COMPONENTES.md` → leé las líneas siguientes.
> 2. Por concepto: `rg -i "transformador|cuadripolo" skill/COMPONENTES.md`.
> 3. Para un **ejemplo real** de un componente: `rg -l "cpts: .*\btf\b" skill/galeria/sch/`
>    o por tag `rg -l "cpt:tf" skill/galeria/sch/`.

**Legenda** `nodos`: cantidad y orden. `fork`: **✅** verificado que dibuja ·
**⚠️** con salvedad. Parámetros modificables (dirección, etiquetas, `kind`, …) → `PARAMETROS.md`.

**Convenciones del autor** R/L/C con símbolo **americano** (zigzag/espiral/paralelas);
**impedancia genérica = `Z` (rectángulo IEC)**, admitancia = `Y`; idioma español;
coma decimal en texto explicativo.

---

## Índice rápido (1 línea por componente)

| comp | id | nodos | qué es | fork |
|---|---|---|---|---|
| `R` | `cpt-r` | 2 | resistencia (zigzag) | ✅ |
| `NR` | `cpt-r` | 2 | resistencia sin ruido (= R, ver `cpt-r`) | ✅ |
| `L` | `cpt-l` | 2 | inductancia (espiral) | ✅ |
| `C` | `cpt-c` | 2 | capacidad (paralelas) | ✅ |
| `Z` | `cpt-z` | 2 | **impedancia genérica (rectángulo)** | ✅ |
| `Y` | `cpt-y` | 2 | admitancia genérica (rectángulo) | ✅ |
| `CPE` | `cpt-cpe` | 2 | elemento de fase constante | ✅ |
| `W` | `cpt-w` | 2 | cable / wire | ✅ |
| `O` | `cpt-o` | 2 | circuito abierto (gap) | ✅ |
| `P` | `cpt-p` | 2 | puerto (bornes) | ✅ |
| `FB` | `cpt-fb` | 2 | ferrite bead | ✅ |
| `REL` | `cpt-rel` | 2 | reluctancia magnética | ✅ |
| `V` | `cpt-v` | 2 | fuente de tensión (dc/ac/step/sin/s/noise) | ✅ |
| `I` | `cpt-i` | 2 | fuente de corriente (idem) | ✅ |
| `BAT` | `cpt-bat` | 2 | batería | ✅ |
| `E` `VCVS` | `cpt-e` | 4 | VCVS (también opamp) | ✅ |
| `F` `CCCS` | `cpt-f` | 2+ctrl | CCCS (control = componente) | ✅ |
| `G` `VCCS` | `cpt-g` | 4 | VCCS | ✅ |
| `H` `CCVS` | `cpt-h` | 2+ctrl | CCVS | ✅ |
| `GY` | `cpt-gy` | 4 | girador | ✅ |
| `E …opamp` | `cpt-opamp` | — | opamp / fdopamp / inamp / amp | ✅ |
| `U` | `cpt-u` | pines | chip/opamp/compuerta/flip-flop/mux | ✅ |
| `TF` | `cpt-tf` | 4+ | transformador (núcleo/tap/multi) | ✅ |
| `K` | `cpt-k` | 2 ind. | acoplamiento mutuo | ✅ |
| `TP` | `cpt-tp` | 4 | cuadripolo genérico (caja) | ✅ |
| `TPZ/Y/H/A/B/G` | `cpt-tpparam` | 4 | cuadripolo con parámetros | ✅ |
| `TL` | `cpt-tl` | 4 | línea de transmisión | ✅ |
| `D` | `cpt-d` | 2 | diodo (+ kinds) | ✅ |
| `Q` | `cpt-q` | 3 (C B E) | transistor BJT | ✅ |
| `M` | `cpt-m` | 3 (D G S) | MOSFET | ✅ |
| `J` | `cpt-j` | 3 (D G S) | JFET | ✅ |
| `TVtriode` | `cpt-tv` | 3 | válvula triodo | ✅ |
| `SW` | `cpt-sw` | 2–3 | llave (no/nc/push/spdt) | ✅ |
| `AM` `VM` | `cpt-meter` | 2 | amperímetro / voltímetro | ✅ |
| `S` | `cpt-s` | forma | caja/círculo/elipse/triángulo/núcleo | ✅ |
| `BL` | `cpt-bl` | 2 | bloque funcional (filtro, vco, …) | ✅ |
| `MX` | `cpt-mx` | 3 | mezclador | ✅ |
| `SP` | `cpt-sp` | 3–4 | punto suma | ✅ |
| `TR` | `cpt-tr` | 2 pines | función de transferencia | ✅ |
| `ADC` `DAC` | `cpt-adcdac` | 2 | conversores (bipolo) | ✅ |
| `A` | `cpt-a` | 1 | anotación (texto en nodo) | ✅ |
| `ANT` | `cpt-ant` | 1 | antena (tx/rx) | ✅ |
| `Cable` | `cpt-cable` | — | cable (coax/twinax/utp/…) | ✅ |
| `XT` | `cpt-xt` | 2 | cristal | ✅ |
| `RV` | `cpt-rv` | 3 | potenciómetro | ✅ |
| `FS` `MT` `MISC` | `cpt-misc` | 2 | fusible / motor / genérico circuitikz | ✅ |
| `k` `m` `r` | `cpt-mec` | 2 | resorte / masa / amortiguador | ✅ |

---

## Pasivos

### `R` — resistencia
`id: cpt-r` · nodos: 2 · fork: ✅
- **sintaxis** `R Np Nm [valor]` · sin valor → símbolo = nombre.
- **dibujo** zigzag americano. `kind=variable`/`tunable`. `NR` = versión sin ruido (idéntica al dibujo).
- **ejemplo** `R1 1 2 1k; right` · `R 6 0_6; down, l=R_a`
- **galería** `rg -l "cpt:r" skill/galeria/sch/01_pasivos/` · **ver** `cpt-z` · `param-kind`

### `L` — inductancia
`id: cpt-l` · nodos: 2 · fork: ✅
- **sintaxis** `L Np Nm [valor] [i0]` · `i0` = corriente inicial (no afecta el dibujo).
- **dibujo** espiral. `kind=`: `variable` `choke` `twolineschoke` `tunable` `sensor` `american` `european`.
- **ejemplo** `L1 2 3 10m; right` · **ver** `cpt-c` · `cpt-k`

### `C` — capacidad
`id: cpt-c` · nodos: 2 · fork: ✅
- **sintaxis** `C Np Nm [valor] [v0]` · `v0` = tensión inicial.
- **dibujo** dos paralelas. `kind=`: `electrolytic` `polar` `variable` `curved` `sensor` `tunable`.
- **ejemplo** `C1 3 0 100n; down` · `C1 1 0; down, kind=electrolytic`

### `Z` — impedancia genérica
`id: cpt-z` · nodos: 2 · fork: ✅
- **sintaxis** `Z Np Nm [valor]` · **dibujo** **rectángulo IEC** (la forma preferida del autor para impedancias). No depende de `style`.
- **ejemplo** `Z1 1 2; right, l=Z_a` · **ver** `cpt-y` · `cpt-r`

### `Y` — admitancia genérica
`id: cpt-y` · nodos: 2 · fork: ✅
- **sintaxis** `Y Np Nm [valor]` · **dibujo** rectángulo. **ejemplo** `Y1 1 2; right, l=Y_a`

### `CPE` — elemento de fase constante
`id: cpt-cpe` · nodos: 2 · fork: ✅
- **sintaxis** `CPE Np Nm [valor] [power=1]` · **ejemplo** `CPE1 1 0; down, l=Q`

### `W` — cable / wire
`id: cpt-w` · nodos: 2 · fork: ✅
- **sintaxis** `W Np Nm` (autonombrable). **dibujo** línea sin etiqueta. Acarrea atributos de tierra/alimentación/señal y `steps`/`startarrow`/`endarrow`.
- **ejemplo** `W 0_1 0_2; right` · **ver** `param-steps` · `param-ground`

### `O` — circuito abierto
`id: cpt-o` · nodos: 2 · fork: ✅
- **sintaxis** `O Np Nm` · **dibujo** gap (hueco); útil para **alinear** y poner etiquetas de tensión. **ejemplo** `O 1 2; right=2`

### `P` — puerto
`id: cpt-p` · nodos: 2 · fork: ✅
- **sintaxis** `P Np Nm` · **dibujo** bornes (círculos), como un open con marca de puerto. **ejemplo** `P1 1 0; down, v=V_1`

### `FB` — ferrite bead
`id: cpt-fb` · nodos: 2 · fork: ✅ · **ejemplo** `FB1 1 2; right`

### `REL` — reluctancia
`id: cpt-rel` · nodos: 2 · fork: ✅ · **ejemplo** `REL1 1 2; right` (alias `RL`)

---

## Fuentes independientes

### `V` — fuente de tensión
`id: cpt-v` · nodos: 2 · fork: ✅
- **sintaxis / formas** `V Np Nm [valor]` (DC) · `V .. dc V` · `V .. ac [A] [fase] [w]` · `V .. step V` · `V .. sin Vo Va fo [td] [alpha]` · `V .. s V` (dominio s) · `V .. noise`.
- **dibujo** círculo (fuente). DC por defecto.
- **ejemplo** `V1 1 0 10; down` · `V1 1 0 ac; down` · `V 1 0 step 20; down` · `V1 1 0 sin 0 10 50; down`
- **ver** `cpt-i` · notación de valores (abajo)

### `I` — fuente de corriente
`id: cpt-i` · nodos: 2 · fork: ✅
- **sintaxis / formas** iguales a `V` (`dc/ac/step/sin/s/noise`). **Convención**: la corriente entra por el nodo positivo.
- **dibujo** círculo con flecha. **ejemplo** `I1 0 1 ac; up` · `Iin 1 0 {6*u(t)}; down`

### `BAT` — batería
`id: cpt-bat` · nodos: 2 · fork: ✅ · **ejemplo** `BAT1 1 2; right, kind=cell1`

---

## Fuentes controladas

### `E` / `VCVS` — fuente de tensión controlada por tensión
`id: cpt-e` · nodos: 4 (`Np Nm Ncp Ncm`) · fork: ✅
- **significado** v(Np,Nm) = μ·v(Ncp,Ncm). **dibujo** rombo. **ejemplo** `E1 1 2 3 4 mu; up`
- **ver** `cpt-opamp` (E con kind opamp)

### `F` / `CCCS` — fuente de corriente controlada por corriente
`id: cpt-f` · nodos: 2 + componente de control · fork: ✅
- **sintaxis** `F Np Nm Vcontrol [beta]` · la corriente de control es la que pasa por el **componente nombrado** `Vcontrol` (típicamente una `V` o un `W`).
- **ejemplo** `F1 3 0 V1 beta; up`

### `G` / `VCCS` — fuente de corriente controlada por tensión
`id: cpt-g` · nodos: 4 (`Np Nm Ncp Ncm`) · fork: ✅
- **significado** i = gm·v(Ncp,Ncm). **ejemplo** `G1 1 0 nc+ nc- gm; down`

### `H` / `CCVS` — fuente de tensión controlada por corriente
`id: cpt-h` · nodos: 2 + componente de control · fork: ✅
- **sintaxis** `H Np Nm Vcontrol [R]` · v = R·i(Vcontrol). **ejemplo** `H1 1 0 V1 R; down`

### `GY` — girador
`id: cpt-gy` · nodos: 4 · fork: ✅ · **sintaxis** `GY Np Nm Ncp Ncm [R]` · **ejemplo** `GY1 1 2 3 4 R; right`

---

## Opamp y amplificadores

### `E …opamp` — opamp y familia
`id: cpt-opamp` · nodos: variable · fork: ✅
- **opamp** `E Np Nm opamp Ncp Ncm [Ad] [Ac=0] [Ro=0]` → triángulo con `+`/`−`. `Ncp`=`+`, `Ncm`=`−`.
- **fdopamp** (totalmente diferencial) `E Np Nm fdopamp Ncp Ncm Nocm [Ad] [Ac]`.
- **inamp** (instrumentación) `E Np Nm inamp Ncp Ncm NRp NRm [Ad] [Ac] [Rf]`.
- **amp** `E Np Nm amp Ncp Ncm [Ad] [Ac]`.
- **ejemplo** `E1 out 0 opamp inp inm A; right` · invertir entradas con `mirror`/`mirrorinputs`.
- **ver** `cpt-u` (opamp como chip `U`) · `param-mirror`

---

## Magnéticos

### `TF` — transformador ideal
`id: cpt-tf` · nodos: 4 (`Np Nm Ncp Ncm` = sec+ sec− prim+ prim−) · fork: ✅
- **sintaxis** `TF Np Nm Ncp Ncm [Ns=1] [Np=1]` · el **signo** del número de vueltas decide el lado del punto.
- **variantes** `TFcore` (núcleo) · `TFtap`/`TFtapcore` (con toma, +2 nodos) · `TFscs` (2 dev.) · `TFscss` (3 dev.) · `TFsscss` (4 dev.).
- **dibujo** dos espiras acopladas; relación de vueltas con `l={N_1:N_2}`. Funciona hasta DC.
- **ejemplo** `TF 1 0 2 0; right, l={N_1:N_2}` · `TF 1 0 2 0; right, core=true`
- **ver** `cpt-k` · `param-core`

### `K` — acoplamiento mutuo
`id: cpt-k` · nodos: ninguno (dos **nombres de inductores**) · fork: ✅
- **sintaxis** `K Lname1 Lname2 [k]` · acopla dos inductancias ya definidas; `L1` a la izquierda, `L2` a la derecha.
- **ejemplo** `L1 1 0; down` … `L2 2 0; down` … `K L1 L2 0.9`

---

## Cuadripolos / dos puertos

### `TP` — cuadripolo genérico (caja negra)
`id: cpt-tp` · nodos: 4 (`Np Nm Ncp Ncm` = sal+ sal− ent+ ent−) · fork: ✅
- **dibujo** rectángulo con texto (caja). `shape=cloud` → nube (red indefinida).
- **uso** cuando NO se quiere mostrar la topología interna (abstracción dos-puertos).
- **ejemplo** `TP1 1 2 3 4; right, l=Red\ R` · **ver** `cpt-tpparam` · `param-shape`

### `TPZ` `TPY` `TPH` `TPA` `TPB` `TPG` — cuadripolo con parámetros
`id: cpt-tpparam` · nodos: 4 · fork: ✅
- **sintaxis** `TP? Np Nm Ncp Ncm <Z|Y|H|A|B|G> ?11 ?12 ?21 ?22 [s1] [s2]` · la letra elige el juego de parámetros y siguen las 4 entradas de la matriz (más 2 términos fuente opcionales).
- **ejemplo** `TPZ 1 2 3 4 Z {Z11} {Z12} {Z21} {Z22}; right`
- **nota** distinto del cuadripolo armado con `Z` en T/π (que muestra la estructura interna).

### `TL` — línea de transmisión
`id: cpt-tl` · nodos: 4 · fork: ✅
- **sintaxis** `TL Np Nm Ncp Ncm [Z0] [gamma] [longitud]` · `TLlossless` para sin pérdidas. Atributo `nowires`.
- **ejemplo** `TL1 1 2 3 4; right=2`

---

## Semiconductores

### `D` — diodo
`id: cpt-d` · nodos: 2 (ánodo, cátodo) · fork: ✅
- **dibujo** triángulo + barra. `kind=`: `schottky` `led` `zener` `zzener` `tunnel` `photo` `varcap` `bidirectional` `tvs` `laser`.
- **ejemplo** `D1 1 2; right` · `D1 1 2; right, kind=schottky`

### `Q` — transistor BJT
`id: cpt-q` · nodos: 3 en orden **C B E** · fork: ✅
- **sintaxis** `Q Nc Nb Ne [npn|pnp]` (npn por defecto). **ejemplo** `Q1 c b e npn; up`

### `M` — MOSFET
`id: cpt-m` · nodos: 3 en orden **D G S** · fork: ✅
- **sintaxis** `M Nd Ng Ns [nmos|pmos]` · `kind=` extra: `nfet` `pfet` `nfetd` `pfetd` `nigfete` `hemt` … · atributos `bodydiode` `arrowmos` `bulksource`.
- **ejemplo** `M1 d g s nmos; up` · `M1 0 1 2; right, kind=nfet, bodydiode`

### `J` — JFET
`id: cpt-j` · nodos: 3 (**D G S**) · fork: ✅ · **sintaxis** `J Nd Ng Ns [njf|pjf]` · **ejemplo** `J1 d g s njf; up`

### `TVtriode` — válvula triodo
`id: cpt-tv` · nodos: 3 (ánodo, grilla, cátodo) · fork: ✅ · **ejemplo** `TV1 a g k; up`

---

## Interruptores

### `SW` — llave
`id: cpt-sw` · nodos: 2 (3 para spdt) · fork: ✅
- **variantes** `SW` / `SWno` (normalmente abierta) · `SWnc` (normalmente cerrada) · `SWpush` (pulsador) · `SWspdt` (`SW Nc Np Nm spdt`, 3 nodos).
- **ejemplo** `SW1 1 2; right, no` · `SW1 1 2 3 spdt; right`

---

## Medidores

### `AM` / `VM` — amperímetro / voltímetro
`id: cpt-meter` · nodos: 2 · fork: ✅ · **ejemplo** `AM 1 2; right=1.5` · `VM 2 0; down`

---

## Chips, lógica, formas, bloques

### `U` — chip / opamp / compuerta / flip-flop / mux
`id: cpt-u` · nodos: por pines (`Uname.pin`) · fork: ✅
- **keywords** `opamp` `fdopamp` `inamp` `isoamp` `amp` `buffer` `inverter` `regulator` `adc` `dac` `diffamp` `diffdriver` · compuertas `and` `or` `nand` `nor` `xor` `xnor` · flip-flops `dff` `jkff` `rslatch` · mux `mux21` `mux41` `mux42` · cajas `box`/`circle`/`chipWXYZ` (`chip2121`, …).
- **ejemplo** `U1 opamp; right` · `U1 chip2121; right=2, l=MCU` · `U1 and; right`
- **ver** `param-pins`

### `S` — formas (caja/círculo/elipse/triángulo/núcleo)
`id: cpt-s` · forma con pines · fork: ✅
- **variantes** `Sbox` `Scircle` `Sellipse` `Striangle` `Score`. **ejemplo** `S1 box; right=4, t=H(s)`

### `BL` — bloque funcional
`id: cpt-bl` · nodos: 2 · fork: ✅
- **kind=** `lowpass` `highpass` `bandpass` `lowpass2` `highpass2` `amp` `vco` `adc` `dac` `dcdc` `dcac` `acdc` `piattenuator` `tattenuator` `phaseshifter` `dsp` `fft` `twoport`.
- **ejemplo** `BL1 1 2; right, kind=lowpass`

### `MX` — mezclador
`id: cpt-mx` · nodos: 3 · fork: ✅ · **ejemplo** `MX1 1 2 3; right`

### `SP` — punto suma
`id: cpt-sp` · nodos: 3–4 · fork: ✅
- **variantes** `SPpp` `SPpm` `SPppp` `SPpmm` `SPppm` (los signos fijan `+`/`−` de cada entrada). **ejemplo** `SP1 pm 1 2 3; right`

### `TR` — función de transferencia
`id: cpt-tr` · nodos: 2 pines (entrada, salida) · fork: ✅ · **ejemplo** `TR1 1 2 H; right=1.5`

### `ADC` / `DAC` — conversores (bipolo)
`id: cpt-adcdac` · nodos: 2 · fork: ✅ · **ejemplo** `ADC1 1 2; right` (también como chip `U .. adc`)

---

## Misceláneos

### `A` — anotación
`id: cpt-a` · nodos: 1 · fork: ✅ · **qué es** un texto/marcador anclado a un nodo (no es una forma genérica). **ejemplo** `A1 1; l=hola, anchor=north`

### `ANT` — antena
`id: cpt-ant` · nodos: 1 · fork: ✅ · **ejemplo** `ANT1 1; up, kind=tx`

### `Cable` — cable
`id: cpt-cable` · fork: ✅ · **kind=** `coax` `twinax` `twistedpair` `shieldedtwistedpair` `tline`. **ejemplo** `Cable1; right=2, kind=coax`

### `XT` — cristal
`id: cpt-xt` · nodos: 2 · fork: ✅ · **ejemplo** `XT1 1 2; right`

### `RV` — potenciómetro
`id: cpt-rv` · nodos: 3 (el 3.º es el cursor) · fork: ✅ · **ejemplo** `RV1 1 2 3; right`

### `FS` / `MT` / `MISC` — fusible / motor / genérico
`id: cpt-misc` · nodos: 2 · fork: ✅ · `MISC` dibuja un bipolo circuitikz arbitrario con `kind=` (`thermistor`, `memristor`). **ejemplo** `MISC1 1 2; right, kind=thermistor`

---

## Mecánicos (analogía mecánica)

### `k` / `m` / `r` — resorte / masa / amortiguador
`id: cpt-mec` · nodos: 2 · fork: ✅
- **sintaxis** `k Np Nm [k] [f0]` (resorte) · `m Np Nm [m] [u0]` (masa, un terminal a tierra) · `r Np Nm [r]` (amortiguador). Analogía: fuerza↔corriente, velocidad↔tensión.
- **ejemplo** `m 3 0; right` · `k 1 2; right` · `r 2 3; right`

---

## Notación de valores y expresiones

| forma | interpretación | fork |
|---|---|---|
| `1k` `2.2u` `100n` `10m` `4k7` | número + prefijo SI (`f p n u m k M G T`) | ✅ |
| `Meg` | mega (10⁶), alias SPICE | ✅ |
| `1e-6` | notación científica | ✅ |
| `R_a` `Z_{eq}` | símbolo (no se formatea como valor) | ✅ |
| `{expresión}` | expresión sympy literal (`{10/s}`, `{2*cos(5*t)}`, `{6*u(t)}`) | ✅ |
| `dc V` | continua de valor V | ✅ |
| `ac [A] [fase] [w]` | senoidal (amplitud, fase, ω opcionales) | ✅ |
| `step V` | escalón de amplitud V | ✅ |
| `sin Vo Va fo [td] [alpha]` | senoidal con offset/amplitud/frecuencia | ✅ |
| `s V` | fuente en dominio s | ✅ |
| `noise` | fuente de ruido | ✅ |

> El **formato de presentación** del valor usa la familia `eng` (ver
> `gl-label_value_style`; `sci`/`spice` no están en el fork). Para unidades dentro
> de la etiqueta: `l={50\,$\Omega$}`, `v={5\,kV}` (ver `lbl-comas`).

## Diferencias con lcapy upstream

- Sin análisis simbólico (Laplace/Fourier/MNA): solo **dibujo**. `Schematic` se
  importa directo; `Circuit` no existe (usar `Schematic` con string-netlist).
- Formato de valor reducido a la familia **`eng`** (`gl-label_value_style`).
- La **sintaxis de netlist es 100 % compatible** con lcapy: los ~500 ejemplos de
  `skill/galeria/` se espejan tal cual del repo upstream (497/500 renderizan; ver
  `galeria/RENDER_REPORT.md`).
