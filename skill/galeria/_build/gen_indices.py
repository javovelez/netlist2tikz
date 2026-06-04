#!/usr/bin/env python3
"""Genera galeria/<tema>.md (galería visual por tema) y galeria/README.md."""
import os, json
from collections import Counter

import os as _os
REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", ".."))
GAL = os.path.join(REPO, "skill", "galeria")

THEME = {
 "00_curricular": ("Curriculares del autor (loop-safe, convenciones propias)", "tcii"),
 "01_pasivos": ("Pasivos R/L/C, Z/Y, básicos", "tcii"),
 "02_fuentes": ("Fuentes independientes y controladas", "tcii"),
 "03_diodos": ("Diodos", None),
 "04_transistores": ("Transistores BJT/MOSFET/JFET", None),
 "05_opamps": ("Amplificadores operacionales", "tcii"),
 "06_magneticos": ("Magnéticos: transformadores, acoplamiento mutuo", "tcii"),
 "07_cuadripolos": ("Cuadripolos / dos puertos", "tcii"),
 "08_redes": ("Redes: escaleras, secciones L/T/π, Foster", "tcii"),
 "09_analisis": ("Circuitos de análisis (malla / nodal)", "tcii"),
 "10_simplificacion": ("Simplificación de circuitos", "tcii"),
 "11_switches": ("Llaves y transitorios conmutados", "tcii"),
 "12_logica": ("Lógica: compuertas, flip-flops, multiplexores", "senales"),
 "13_formas_bloques": ("Formas, bloques, mezcladores, sumadores", "senales"),
 "14_diagramas_bloques": ("Diagramas de bloques / realimentación", "senales"),
 "15_dsp_fir": ("DSP / FIR / tiempo discreto", "senales"),
 "16_chips_ic": ("Chips, ICs, MCUs, reguladores, ADC/DAC", None),
 "17_cmos": ("Modelado CMOS", None),
 "18_lineas_transmision": ("Líneas de transmisión, cables, antenas, cristales", None),
 "19_medidores": ("Medidores (amperímetro / voltímetro)", "tcii"),
 "20_tierras_alimentacion": ("Tierras, alimentación, conexiones implícitas", "tcii"),
 "21_etiquetas": ("Etiquetas, anotaciones, V/I/F, estilos de cable", "tcii"),
 "22_intro": ("Introducción / quickstart", "tcii"),
 "23_otros": ("Otros / transductores / varios", None),
}

def main():
    manifest = json.load(open(os.path.join(GAL, "manifest.json")))
    rstat = json.load(open(os.path.join(GAL, "render_status.json")))
    by_theme = {}
    for m in manifest:
        by_theme.setdefault(m["theme"], []).append(m)

    counts = {}
    for theme, (label, curr) in THEME.items():
        items = sorted(by_theme.get(theme, []), key=lambda m: m["base"].lower())
        counts[theme] = len(items)
        lines = [f"# {label}", "",
                 f"Tema `{theme}` · **{len(items)}** ejemplos. "
                 f"Espejados de lcapy (LGPL). Buscá por tag con "
                 f"`rg -l \"n2t-tags:.*<tag>\" sch/{theme}/`.", ""]
        if curr:
            lines.append(f"> Curricular: **{ 'Teoría de Circuitos II' if curr=='tcii' else 'Análisis de Señales y Sistemas'}**")
            lines.append("")
        lines += ["| ejemplo | componentes | tags | vista |", "|---|---|---|---|"]
        for m in items:
            png = m["file"][:-4] + ".png"
            ok = rstat.get(m["file"], "?") == "ok"
            vista = f"![]({os.path.relpath(os.path.join(GAL, png), GAL)})" if ok else "⚠️ no renderiza"
            sem = [t for t in m["tags"]
                   if not t.startswith("cpt:") and not t.startswith("curricular:")]
            cptstr = ",".join(m.get("ctypes", [])) or "—"
            title = m["title"].replace("|", "/")
            lines.append(f"| [{m['id']}]({m['file']}) · {title} | {cptstr} | "
                         f"{', '.join(sem[:8])} | {vista} |")
        open(os.path.join(GAL, f"{theme}.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

    # README
    ok = sum(1 for v in rstat.values() if v == "ok")
    tot = len(rstat)
    curric = {"tcii": [], "senales": []}
    for theme, (label, curr) in THEME.items():
        if curr:
            curric[curr].append((theme, label))
    R = ["# Galería de ejemplos — netlist2tikz", "",
         f"Espejo navegable de **{len(manifest)}** esquemáticos de la documentación de "
         f"[lcapy](https://github.com/mph-/lcapy) (LGPL-2.1), reproducidos con este fork "
         f"(**{ok}/{tot}** renderizan; ver [RENDER_REPORT.md](RENDER_REPORT.md)).", "",
         "## Cómo buscar", "",
         "- **Por tag**: `rg -l \"n2t-tags:.*resonancia\" sch/` (lista archivos).",
         "- **Por componente**: `rg -l \"cpt:tf\" sch/` · **por kind**: `rg -l \"kind:schottky\" sch/`.",
         "- **Índice máquina**: [index.tsv](index.tsv) (id · tema · archivo · título · tags · cpts · params).",
         "- **Vocabulario de tags** y mapa intención→componente: ver [`../INDICE.md`](../INDICE.md).",
         "- Cada `.sch` trae un header `# n2t-id:` / `# n2t-tags:` con sus metadatos.", "",
         "## Ruta curricular", ""]
    R.append("**Teoría de Circuitos II** → " +
             " · ".join(f"[{l}]({t}.md)" for t, l in curric["tcii"]))
    R.append("")
    R.append("**Análisis de Señales y Sistemas** → " +
             " · ".join(f"[{l}]({t}.md)" for t, l in curric["senales"]))
    R += ["", "## Todos los temas", "", "| tema | ejemplos | |", "|---|--:|---|"]
    for theme, (label, curr) in THEME.items():
        tag = " · ⭐ curricular" if curr else ""
        R.append(f"| [{theme}]({theme}.md) | {counts[theme]} | {label}{tag} |")
    R += ["", "## Regenerar",
          "```bash", "python render.py        # re-render PNG + RENDER_REPORT.md", "```",
          "", "Atribución: netlists © 2014–2026 Michael Hayes (UCECE), lcapy, LGPL-2.1."]
    open(os.path.join(GAL, "README.md"), "w", encoding="utf-8").write("\n".join(R) + "\n")
    print(f"Generados {len(THEME)} índices de tema + README. Total {len(manifest)} ejemplos.")
    print("Conteos:", dict(sorted(counts.items())))

if __name__ == "__main__":
    main()
