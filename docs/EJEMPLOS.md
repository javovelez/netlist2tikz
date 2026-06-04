# Galería de ejemplos → movida a la skill

La galería de ejemplos es un **espejo navegable de ~537 esquemáticos**
(todos los de la documentación de lcapy + los curriculares del autor, incluidos
los **16 filtros del TP4 — Teoría Imagen**), con miniaturas, tags y un índice máquina.
Vive con la skill:

- **[../skill/galeria/README.md](../skill/galeria/README.md)** — 24 temas, ruta curricular,
  cómo buscar.
- **[../skill/galeria/index.tsv](../skill/galeria/index.tsv)** — índice máquina
  (id · tema · archivo · título · tags · cpts · params).
- **[../skill/galeria/RENDER_REPORT.md](../skill/galeria/RENDER_REPORT.md)** — qué reproduce
  el fork (los `.png` se regeneran con `python skill/galeria/render.py`).

Buscar un ejemplo: `rg -l "n2t-tags:.*resonancia" ../skill/galeria/sch/`.
Los filtros del TP4 están en `00_curricular` con prefijo `tp4_`:
`rg -l "tp4-" ../skill/galeria/sch/` (prototipos T, m-derivadas, hemisecciones;
pasabajos/pasaaltos/pasabanda/suprimebanda; y el esquema de cuadripolos en cascada).
Cada `.sch` se puede renderizar con `n2t render <archivo> -o salida.pdf`.
