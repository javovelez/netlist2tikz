#!/usr/bin/env python3
"""Deriva tags controlados y prepende header de metadatos a cada .sch. Emite index.tsv."""
import os, re, json

import os as _os
REPO = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", ".."))
GAL = os.path.join(REPO, "skill", "galeria")

THEME_META = {
 "00_curricular": ("Curriculares del autor (loop-safe, convenciones propias)", "curricular-base", "tcii"),
 "01_pasivos": ("Pasivos R/L/C, Z/Y, básicos", "pasivo", "tcii"),
 "02_fuentes": ("Fuentes independientes y controladas", "fuente", "tcii"),
 "03_diodos": ("Diodos", "diodo", None),
 "04_transistores": ("Transistores BJT/MOSFET/JFET", "transistor", None),
 "05_opamps": ("Amplificadores operacionales", "opamp", "tcii"),
 "06_magneticos": ("Magnéticos: transformadores, acoplamiento", "magnetico", "tcii"),
 "07_cuadripolos": ("Cuadripolos / dos puertos", "cuadripolo", "tcii"),
 "08_redes": ("Redes: escaleras, L/T/π, Foster", "red", "tcii"),
 "09_analisis": ("Circuitos de análisis (malla/nodal)", "analisis", "tcii"),
 "10_simplificacion": ("Simplificación de circuitos", "simplificacion", "tcii"),
 "11_switches": ("Llaves y transitorios conmutados", "switch", "tcii"),
 "12_logica": ("Lógica: compuertas, flip-flops, mux", "logica", "senales"),
 "13_formas_bloques": ("Formas, bloques, mezcladores, sumadores", "bloque", "senales"),
 "14_diagramas_bloques": ("Diagramas de bloques / realimentación", "diagrama-bloques", "senales"),
 "15_dsp_fir": ("DSP / FIR / tiempo discreto", "dsp", "senales"),
 "16_chips_ic": ("Chips, ICs, MCUs, reguladores, ADC/DAC", "chip", None),
 "17_cmos": ("Modelado CMOS", "cmos", None),
 "18_lineas_transmision": ("Líneas de transmisión, cables, antenas, cristales", "linea-transmision", None),
 "19_medidores": ("Medidores (amperímetro / voltímetro)", "medidor", "tcii"),
 "20_tierras_alimentacion": ("Tierras, alimentación, conexiones implícitas", "tierra", "tcii"),
 "21_etiquetas": ("Etiquetas, anotaciones, V/I/F, estilos de cable", "etiqueta", "tcii"),
 "22_intro": ("Introducción / quickstart", "intro", "tcii"),
 "23_otros": ("Otros / transductores / varios", "varios", None),
}

PREFIX = [('TPZ','tp'),('TPY','tp'),('TPH','tp'),('TPG','tp'),('TPB','tp'),('TPA','tp'),('TP','tp'),
 ('TFtapcore','tf'),('TFtap','tf'),('TFcore','tf'),('TFsscss','tf'),('TFscss','tf'),('TFscs','tf'),('TF','tf'),
 ('TLlossless','tl'),('TL','tl'),('TVtriode','triodo'),('TV','triodo'),('TR','tr'),
 ('SWspdt','sw'),('SWnc','sw'),('SWno','sw'),('SWpush','sw'),('SW','sw'),
 ('CPE','cpe'),('FB','fb'),('XT','xt'),('NR','r'),('GY','gy'),('REL','rel'),('RL','rel'),('RV','rv'),
 ('AM','am'),('VM','vm'),('ANT','ant'),('BAT','bat'),('BL','bl'),('MX','mx'),('SP','sp'),
 ('ADC','adc'),('DAC','dac'),('MISC','misc'),('VCVS','e'),('VCCS','g'),('CCCS','f'),('CCVS','h'),
 ('Cable','cable'),('U','u')]
SINGLE = set('RLCZYVIEFGHDQMJKWOPAS')

def cpt_type(name):
    for pre, t in PREFIX:
        if name.startswith(pre):
            return t
    if name[:1] == 's' and name[1:2] in ('V', 'I'):
        return name[1].lower()
    if name[:1] in SINGLE:
        return name[0].lower() if name[0] != 'S' else 'shape'
    if name[:1] in ('k', 'm', 'r'):
        return 'mecanico'
    return None

VSET = {'v', 'v^', 'v_', 'v<', 'v>', 'v^>', 'v^<', 'v_>', 'v_<'}
ISET = {'i','i<','i<^','i<_','i>','i>^','i>_','i^','i^<','i^>','i_','i_<','i_>','ir'}
FSET = {'f','f<','f<^','f<_','f>^','f>_','f^<','f^>','f_<','f_>','f^','f_','f>','f<^'}
PARAM_TAG = {
 'l':'etiqueta','l^':'etiqueta','l_':'etiqueta','t':'etiqueta',
 'a':'anotacion','a_':'anotacion','a^':'anotacion',
 'color':'estilo','fill':'estilo','blue':'estilo','purple':'estilo','dashed':'estilo',
 'dotted':'estilo','thick':'estilo','ultra thick':'estilo','line width':'estilo','fill opacity':'estilo',
 'kind':'kind','variable':'kind','core':'kind','bodydiode':'kind','arrowmos':'kind',
 'bulksource':'kind','bulk':'kind',
 'shape':'forma','aspect':'forma','width':'forma','image':'imagen',
 'mirror':'espejo','invert':'espejo','fliplr':'espejo','flipud':'espejo','mirrorinputs':'espejo','reverse':'espejo',
 'rotate':'rotacion',
 'offset':'layout','free':'layout','fixed':'layout','steps':'layout','startarrow':'layout',
 'endarrow':'layout','nowires':'layout','arrow':'layout',
 'ground':'tierra','sground':'tierra','cground':'tierra','nground':'tierra','pground':'tierra',
 'rground':'tierra','tground':'tierra','tlground':'tierra','eground':'tierra','eground2':'tierra',
 '0V':'tierra','implicit':'tierra','autoground':'tierra',
 'vdd':'alimentacion','vss':'alimentacion','vcc':'alimentacion','vee':'alimentacion',
 'input':'pad-senal','output':'pad-senal','bidir':'pad-senal','pad':'pad-senal','bus':'pad-senal',
 'draw_nodes':'visibilidad-nodos','label_nodes':'visibilidad-nodos','nodes':'visibilidad-nodos',
 'label_ids':'etiquetas-globales','label_values':'etiquetas-globales','label_style':'etiquetas-globales',
 'label_value_style':'etiquetas-globales','label_flip':'etiquetas-globales','draw_labels':'etiquetas-globales',
 'style':'estilo-simbolo',
 'cpt_size':'geometria-global','node_spacing':'geometria-global','scale':'geometria-global',
 'help_lines':'grilla','voltage_dir':'convencion',
 'pindefs':'pines','pinlabels':'pines','pinnames':'pines','pinnodes':'pines','anchor':'pines','anchors':'pines',
 'nosim':'control','nodraw':'control','invisible':'control','ignore':'control',
}
def param_tag(p):
    if p in VSET: return 'etiqueta-v'
    if p in ISET: return 'etiqueta-i'
    if p in FSET: return 'etiqueta-f'
    if p.startswith('.'):
        seg = p.split('.')[-1]
        if seg in ('vdd','vss','vcc','vee'): return 'alimentacion'
        if seg == 'implicit': return 'tierra'
        if seg in ('input','output','bidir','pad'): return 'pad-senal'
        if seg == 'l': return 'etiqueta-nodo'
        if seg == 'fill': return 'estilo'
        return 'nodo-pin'
    return PARAM_TAG.get(p)

# Descripciones/títulos curados para los más relevantes (curricular). Resto: nombre prettificado.
TITLE = {
 'RC1':'RC serie horizontal','RC2':'R y C en paralelo (par vertical)','LC1':'LC a tierra',
 'voltage-divider':'Divisor de tensión','voltage-divider2':'Divisor de tensión (variante)',
 'twoport1':'Cuadripolo genérico (caja)','twoport2':'Cuadripolo genérico (variante)',
 'opamp-inverting-amplifier':'Opamp inversor','opamp-noninverting-amplifier':'Opamp no inversor',
 'opamp-inverting-integrator':'Integrador con opamp','ladder':'Red en escalera',
 'tsection':'Sección en T','pisection':'Sección en π','lsection':'Sección en L',
 'TF1':'Transformador ideal','TFcore1':'Transformador con núcleo','K1':'Acoplamiento mutuo',
 'current_labels1':'Etiquetas de corriente (todas las variantes)',
 'voltage_labels1':'Etiquetas de tensión','flow_labels1':'Etiquetas de flujo',
 'grounds':'Tipos de tierra','supplies':'Rieles de alimentación','switches':'Tipos de llave',
 'diodes':'Tipos de diodo','transistors':'Tipos de transistor','resistors':'Resistencias (variantes)',
}
def pretty(base):
    if base in TITLE: return TITLE[base]
    s = re.sub(r'[_\-]+', ' ', base).strip()
    return s[:1].upper() + s[1:]

def main():
    manifest = json.load(open(os.path.join(GAL, "manifest.json")))
    rows = []
    for m in manifest:
        theme = m["theme"]
        tlabel, ttag, curr = THEME_META[theme]
        tags = {ttag}
        if curr: tags.add(f"curricular:{curr}")
        ctypes = sorted({t for n in m["cpts"] if (t := cpt_type(n))})
        for t in ctypes: tags.add(f"cpt:{t}")
        for p in m["params"]:
            pt = param_tag(p)
            if pt: tags.add(pt)
        for k in m["kinds"]:
            tags.add(f"kind:{k}")
        if m.get("raw"): tags.add("raw-tikz")
        title = pretty(m["base"])
        tagstr = ", ".join(sorted(tags))
        cptstr = ",".join(ctypes)
        m["tags"] = sorted(tags); m["title"] = title; m["ctypes"] = ctypes
        # prepend header (cuerpo idéntico a upstream)
        path = os.path.join(GAL, m["file"])
        body = open(path, encoding="utf-8", errors="replace").read()
        header = (f"# n2t-id: {m['id']}  ·  {title}\n"
                  f"# n2t-tags: {tagstr}  ·  cpts: {cptstr}  ·  src: {m['src']}\n")
        if not body.startswith("# n2t-id:"):
            open(path, "w", encoding="utf-8").write(header + body)
        rows.append((m["id"], theme, m["file"], title, tagstr, cptstr,
                     ",".join(sorted(m["params"]))[:200]))
    json.dump(manifest, open(os.path.join(GAL, "manifest.json"), "w"), ensure_ascii=False, indent=1)
    with open(os.path.join(GAL, "index.tsv"), "w", encoding="utf-8") as f:
        f.write("id\ttheme\tfile\ttitle\ttags\tcpts\tparams\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    allt = sorted({t for m in manifest for t in m["tags"]})
    print(f"{len(manifest)} archivos con header.  {len(allt)} tags únicos.")
    print("Tags:", ", ".join(allt))

if __name__ == "__main__":
    main()
