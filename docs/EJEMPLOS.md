# Galería de ejemplos → movida a la skill

La galería de ejemplos se amplió a un **espejo navegable de ~520 esquemáticos**
(todos los de la documentación de lcapy + los curriculares del autor), con miniaturas,
tags y un índice máquina. Vive con la skill:

- **[../skill/galeria/README.md](../skill/galeria/README.md)** — 24 temas, ruta curricular,
  cómo buscar.
- **[../skill/galeria/index.tsv](../skill/galeria/index.tsv)** — índice máquina
  (id · tema · archivo · título · tags · cpts · params).
- **[../skill/galeria/RENDER_REPORT.md](../skill/galeria/RENDER_REPORT.md)** — qué reproduce
  el fork (497/500 de lcapy + 20/20 curriculares).

Buscar un ejemplo: `rg -l "n2t-tags:.*resonancia" ../skill/galeria/sch/`.
Cada `.sch` se puede renderizar con `n2t render <archivo> -o salida.pdf`.
