# _build — pipeline que arma la galería

Scripts que generaron la galería (reproducibilidad / transparencia del tagging).
Todos derivan la raíz del repo de su propia ubicación; no hace falta editar rutas.

| script | qué hace | cuándo correrlo |
|---|---|---|
| `categorize.py` | espeja los `.sch` de un clon de lcapy a `../sch/<tema>/` y de los templates del autor a `00_curricular`; escribe `manifest.json` con componentes/parámetros/kinds parseados | solo para **re-espejar** desde upstream |
| `build_meta.py` | deriva tags controlados, prepende el header `# n2t-id:` / `# n2t-tags:` a cada `.sch` y emite `../index.tsv` | tras `categorize.py` o si cambia el esquema de tags |
| `gen_indices.py` | regenera los `../<tema>.md` (galería visual) y `../README.md` desde `manifest.json` + `render_status.json` | tras cambios en metadatos o render |
| `../render.py` | re-renderiza todos los `.sch` a PNG + `../RENDER_REPORT.md` | para refrescar miniaturas |

## Re-espejar desde lcapy (raro)

```bash
git clone --depth 1 https://github.com/mph-/lcapy.git /tmp/lcapy_src   # o LCAPY_SRC=<ruta>
python _build/categorize.py        # mirror + manifest
python _build/build_meta.py        # tags + headers + index.tsv
python ../render.py                # PNG + reporte
python _build/gen_indices.py       # índices .md + README
```

## Esquema de tags

Definido en `build_meta.py`: tag de tema, `cpt:<tipo>` por componente,
`kind:<valor>`, tags de feature (etiqueta-v/i/f, tierra, espejo, …) y
`curricular:tcii|senales`. El vocabulario canónico está en `../../INDICE.md`.

Atribución: netlists © 2014–2026 Michael Hayes (UCECE), lcapy, LGPL-2.1.
