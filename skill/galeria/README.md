# Galería de ejemplos — netlist2tikz

Espejo navegable de **537** esquemáticos de la documentación de [lcapy](https://github.com/mph-/lcapy) (LGPL-2.1), reproducidos con este fork (**533/536** renderizan; ver [RENDER_REPORT.md](RENDER_REPORT.md)).

## Cómo buscar

- **Por tag**: `rg -l "n2t-tags:.*resonancia" sch/` (lista archivos).
- **Por componente**: `rg -l "cpt:tf" sch/` · **por kind**: `rg -l "kind:schottky" sch/`.
- **Índice máquina**: [index.tsv](index.tsv) (id · tema · archivo · título · tags · cpts · params).
- **Vocabulario de tags** y mapa intención→componente: ver [`../INDICE.md`](../INDICE.md).
- Cada `.sch` trae un header `# n2t-id:` / `# n2t-tags:` con sus metadatos.

## Ruta curricular

**Teoría de Circuitos II** → [Curriculares del autor (loop-safe, convenciones propias)](00_curricular.md) · [Pasivos R/L/C, Z/Y, básicos](01_pasivos.md) · [Fuentes independientes y controladas](02_fuentes.md) · [Amplificadores operacionales](05_opamps.md) · [Magnéticos: transformadores, acoplamiento mutuo](06_magneticos.md) · [Cuadripolos / dos puertos](07_cuadripolos.md) · [Redes: escaleras, secciones L/T/π, Foster](08_redes.md) · [Circuitos de análisis (malla / nodal)](09_analisis.md) · [Simplificación de circuitos](10_simplificacion.md) · [Llaves y transitorios conmutados](11_switches.md) · [Medidores (amperímetro / voltímetro)](19_medidores.md) · [Tierras, alimentación, conexiones implícitas](20_tierras_alimentacion.md) · [Etiquetas, anotaciones, V/I/F, estilos de cable](21_etiquetas.md) · [Introducción / quickstart](22_intro.md)

**Análisis de Señales y Sistemas** → [Lógica: compuertas, flip-flops, multiplexores](12_logica.md) · [Formas, bloques, mezcladores, sumadores](13_formas_bloques.md) · [Diagramas de bloques / realimentación](14_diagramas_bloques.md) · [DSP / FIR / tiempo discreto](15_dsp_fir.md)

## Todos los temas

| tema | ejemplos | |
|---|--:|---|
| [00_curricular](00_curricular.md) | 36 | Curriculares del autor (loop-safe, convenciones propias) · ⭐ curricular |
| [01_pasivos](01_pasivos.md) | 40 | Pasivos R/L/C, Z/Y, básicos · ⭐ curricular |
| [02_fuentes](02_fuentes.md) | 8 | Fuentes independientes y controladas · ⭐ curricular |
| [03_diodos](03_diodos.md) | 12 | Diodos |
| [04_transistores](04_transistores.md) | 36 | Transistores BJT/MOSFET/JFET |
| [05_opamps](05_opamps.md) | 69 | Amplificadores operacionales · ⭐ curricular |
| [06_magneticos](06_magneticos.md) | 38 | Magnéticos: transformadores, acoplamiento mutuo · ⭐ curricular |
| [07_cuadripolos](07_cuadripolos.md) | 15 | Cuadripolos / dos puertos · ⭐ curricular |
| [08_redes](08_redes.md) | 18 | Redes: escaleras, secciones L/T/π, Foster · ⭐ curricular |
| [09_analisis](09_analisis.md) | 17 | Circuitos de análisis (malla / nodal) · ⭐ curricular |
| [10_simplificacion](10_simplificacion.md) | 10 | Simplificación de circuitos · ⭐ curricular |
| [11_switches](11_switches.md) | 13 | Llaves y transitorios conmutados · ⭐ curricular |
| [12_logica](12_logica.md) | 22 | Lógica: compuertas, flip-flops, multiplexores · ⭐ curricular |
| [13_formas_bloques](13_formas_bloques.md) | 17 | Formas, bloques, mezcladores, sumadores · ⭐ curricular |
| [14_diagramas_bloques](14_diagramas_bloques.md) | 7 | Diagramas de bloques / realimentación · ⭐ curricular |
| [15_dsp_fir](15_dsp_fir.md) | 7 | DSP / FIR / tiempo discreto · ⭐ curricular |
| [16_chips_ic](16_chips_ic.md) | 38 | Chips, ICs, MCUs, reguladores, ADC/DAC |
| [17_cmos](17_cmos.md) | 25 | Modelado CMOS |
| [18_lineas_transmision](18_lineas_transmision.md) | 24 | Líneas de transmisión, cables, antenas, cristales |
| [19_medidores](19_medidores.md) | 2 | Medidores (amperímetro / voltímetro) · ⭐ curricular |
| [20_tierras_alimentacion](20_tierras_alimentacion.md) | 19 | Tierras, alimentación, conexiones implícitas · ⭐ curricular |
| [21_etiquetas](21_etiquetas.md) | 33 | Etiquetas, anotaciones, V/I/F, estilos de cable · ⭐ curricular |
| [22_intro](22_intro.md) | 27 | Introducción / quickstart · ⭐ curricular |
| [23_otros](23_otros.md) | 4 | Otros / transductores / varios |

## Regenerar
```bash
python render.py        # re-render PNG + RENDER_REPORT.md
```

Atribución: netlists © 2014–2026 Michael Hayes (UCECE), lcapy, LGPL-2.1.
