#!/usr/bin/env python3
"""Espeja los .sch de lcapy en galeria/sch/<tema>/ y extrae metadatos para tagging."""
import os, re, shutil, json, sys

SRC = _os.environ.get("LCAPY_SRC", "/tmp/lcapy_src")
import os as _os
REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", ".."))
GAL = os.path.join(REPO, "skill", "galeria")
SCH = os.path.join(GAL, "sch")
TEMPLATES = os.path.join(REPO, "skill", "templates")  # netlists curriculares del autor

# ---- Reglas por ORIGEN (subdir de lcapy) — más confiables para tutoriales ----
ORIGIN_THEME = [
    ("tutorials/opamps",       "05_opamps"),
    ("tutorials/opampnoise",   "05_opamps"),
    ("tutorials/transformers", "06_magneticos"),
    ("tutorials/nonlinear",    "04_transistores"),
    ("tutorials/transducers",  "23_otros"),
    ("tutorials/shield-guard", "18_lineas_transmision"),
    ("tutorials/discretetime", "15_dsp_fir"),
    ("tutorials/annotations",  "21_etiquetas"),
    ("tutorials/RCnoise",      "01_pasivos"),
    ("tutorials/txline",       "18_lineas_transmision"),
    ("tutorials/ivp",          "09_analisis"),
    ("tutorials/basic",        "22_intro"),
    ("schematics/digital",     "16_chips_ic"),
    ("schematics/analogue",    "04_transistores"),
    ("simulation",             "09_analisis"),
    ("networks",               "08_redes"),
    ("latex",                  "21_etiquetas"),
    ("lcapy/tests",            "23_otros"),
]

# ---- Reglas por NOMBRE (basename lower, sin .sch) — orden = prioridad ----
NAME_RULES = [
    (r"cmos",                                              "17_cmos"),
    (r"^(pio|mcu|pic\d|ic\d|i2c|chips|uchip|uregulator|uadc|udac|adc\d|dac\d)", "16_chips_ic"),
    (r"(dff|jkff|rslatch|flipflop|^gates|^u(and|or|nand|nor|xor|xnor|inverter|buffer)|^buffer|multiplexer|umux)", "12_logica"),
    (r"^fir",                                              "15_dsp_fir"),
    (r"(negative-feedback|proportional|^domains|signal-flow|block)", "14_diagramas_bloques"),
    (r"(tline|^cable|antenna|^xt\d|pierce|guard|shield|txline)", "18_lineas_transmision"),
    (r"(opamp|fdopamp|inamp|isoamp|diffamp|integrator|sallen|^lpf1)", "05_opamps"),
    (r"(^tp[a-z0-9]|twoport|^btwoport|^tf_)",              "07_cuadripolos"),
    (r"(^tf\d|^tfcore|^tftap|^tfscs|^tfscss|^tf2|^tf3|^tf4|^k\d|mutual|ideal-tf|^ltft|^stepup|transformers|reluctance|^gy|bh-mag)", "06_magneticos"),
    (r"(^q\d|qnpn|qpnp|^m\d|^j\d|transistor|common-base|accelerometer|^amp$|totem|push_pull|nmosfet)", "04_transistores"),
    (r"(^d\d|^dbridge|^d(down|left|right|up)|diodes)",     "03_diodos"),
    (r"(switch|^sw)",                                      "11_switches"),
    (r"(simplify|inseries)",                               "10_simplificacion"),
    (r"(mesh|^graph|^ss\d|amplifier1|circuit-v|^ladder1|transfer1|^tf2$)", "09_analisis"),
    (r"(ground|autoground|implicit|supplies|batteries|connections|^0v)", "20_tierras_alimentacion"),
    (r"(label|annotate|arrows|current|voltage_label|flow_label|wirestyle|steppedwire|colors|rlabels|fliplr|^attr)", "21_etiquetas"),
    (r"(ladder|lsection|tsection|pisection|rnet|^net\d|seriespair|^series|shunt|^parallel|foster)", "08_redes"),
    (r"(^sp\d|^mx\d|^blocks|^sbox|^scircle|^striangle|^tr1|^misc|frankenstein)", "13_formas_bloques"),
    (r"meters",                                            "19_medidores"),
    (r"(resistor|capacitor|inductor|stamp|^rright|^rc\d|^lc\d|^l\d|^c\d|^cpe|^fb\d|ferrite|massspring|voltage-divider|^vrl|^vacrl|^vrmesh|^vil|^vir|variable1|^seriespair)", "01_pasivos"),
    (r"(vsource|voltage_source|hsource|^v\d|^v-stamp|^i-stamp|^e1|^f1|^g1|^h1)", "02_fuentes"),
]

def theme_for(relpath, base):
    for frag, th in ORIGIN_THEME:
        if frag in relpath:
            return th
    low = base.lower()
    for pat, th in NAME_RULES:
        if re.search(pat, low):
            return th
    return "22_intro"

# ---- Parseo de netlist: componentes, parámetros, kinds ----
CPT_RE = re.compile(r"^([A-Za-z]+)")
def parse_sch(text):
    cpts, params, kinds, has_raw = set(), set(), set(), False
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        if line[:1] in "#%*":
            continue
        if line.lstrip().startswith(";;"):
            has_raw = True
            continue
        # separar cuerpo / opciones
        body, _, opts = line.partition(";")
        body = body.strip()
        if body:
            toks = body.split()
            m = CPT_RE.match(toks[0])
            if m:
                cpts.add(m.group(1))
        for part in re.split(r",(?![^{]*})", opts):  # split por coma fuera de llaves (aprox)
            part = part.strip()
            if not part:
                continue
            key = part.split("=")[0].strip()
            if key:
                params.add(key)
            if key == "kind":
                v = part.split("=", 1)[1].strip() if "=" in part else ""
                if v:
                    kinds.add(v)
    return sorted(cpts), sorted(params), sorted(kinds), has_raw

def main():
    if os.path.isdir(SCH):
        shutil.rmtree(SCH)
    os.makedirs(SCH)
    manifest = []
    seen = {}  # base -> count para colisiones
    for root, _, files in os.walk(SRC):
        for f in sorted(files):
            if not f.endswith(".sch"):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, SRC)
            base = f[:-4]
            th = theme_for(rel, base)
            # nombre destino (evitar colisiones)
            dest_name = f
            if (th, dest_name) in seen:
                seen[(th, dest_name)] += 1
                dest_name = f"{base}__{seen[(th,dest_name)]}.sch"
            else:
                seen[(th, dest_name)] = 0
            dest_dir = os.path.join(SCH, th)
            os.makedirs(dest_dir, exist_ok=True)
            text = open(full, encoding="utf-8", errors="replace").read()
            shutil.copy2(full, os.path.join(dest_dir, dest_name))
            cpts, params, kinds, has_raw = parse_sch(text)
            manifest.append({
                "id": base.lower().replace("_", "-"),
                "theme": th,
                "file": f"sch/{th}/{dest_name}",
                "src": rel,
                "base": base,
                "cpts": cpts, "params": params, "kinds": kinds,
                "raw": has_raw,
                "nlines": len([l for l in text.splitlines() if l.strip() and l[:1] not in "#%*"]),
            })
    # Fuente extra: templates curriculares del autor → tema 00_curricular
    if os.path.isdir(TEMPLATES):
        for f in sorted(os.listdir(TEMPLATES)):
            if not f.endswith(".sch"):
                continue
            full = os.path.join(TEMPLATES, f)
            base = f[:-4]
            th = "00_curricular"
            dest_dir = os.path.join(SCH, th)
            os.makedirs(dest_dir, exist_ok=True)
            text = open(full, encoding="utf-8", errors="replace").read()
            shutil.copy2(full, os.path.join(dest_dir, f))
            cpts, params, kinds, has_raw = parse_sch(text)
            manifest.append({
                "id": base.lower().replace("_", "-"),
                "theme": th, "file": f"sch/{th}/{f}", "src": f"skill/templates/{f}",
                "base": base, "cpts": cpts, "params": params, "kinds": kinds,
                "raw": has_raw,
                "nlines": len([l for l in text.splitlines() if l.strip() and l[:1] not in "#%*"]),
            })

    manifest.sort(key=lambda m: (m["theme"], m["base"].lower()))
    os.makedirs(GAL, exist_ok=True)
    json.dump(manifest, open(os.path.join(GAL, "manifest.json"), "w"), ensure_ascii=False, indent=1)
    # resumen
    from collections import Counter
    c = Counter(m["theme"] for m in manifest)
    print(f"TOTAL: {len(manifest)} archivos\n")
    for th in sorted(c):
        print(f"{c[th]:4d}  {th}")
    print(f"\nComponentes únicos vistos: {sorted(set(x for m in manifest for x in m['cpts']))}")
    print(f"\nParámetros únicos vistos: {sorted(set(x for m in manifest for x in m['params']))}")

if __name__ == "__main__":
    main()
