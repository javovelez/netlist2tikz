# n2t-id: cmos-totem  ·  Cmos totem
# n2t-tags: cmos, cpt:m, cpt:w, etiqueta, etiquetas-globales, pad-senal, tierra, visibilidad-nodos  ·  cpts: m,w  ·  src: doc/examples/schematics/cmos-totem.sch
M1 1 2 3 pmos; right, l=Pull-up (PMOS)
M2 1 4 5 nmos; right, l=Pull-down (NMOS)
W 3 6; up=0.1, sground, l=V_{DD}
W 5 7; down=0.1, sground, l=V_{SS}
W 1 p; right, output, l=PIN
;draw_nodes=connections, label_nodes=none, label_ids=False
