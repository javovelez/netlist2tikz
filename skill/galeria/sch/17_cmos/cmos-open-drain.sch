# n2t-id: cmos-open-drain  ·  Cmos open drain
# n2t-tags: cmos, cpt:m, cpt:r, cpt:w, etiqueta, etiquetas-globales, tierra, visibilidad-nodos  ·  cpts: m,r,w  ·  src: doc/examples/schematics/cmos-open-drain.sch
M 1 2 3; right, l=Pull-down (NMOS)
W 3 0; down=0.1, sground, l=$V_{SS}
W 1 4; right
W 4 5; right
R 4 6; up, l=External pull-up
W 6 7; up=0.1, sground, l=$V_{DD}
;draw_nodes=connections, label_nodes=False, label_ids=False
