# n2t-id: cmos-input-model2  ·  Cmos input model2
# n2t-tags: cmos, cpt:c, cpt:p, cpt:r, cpt:v, cpt:w, etiqueta, etiquetas-globales, visibilidad-nodos  ·  cpts: c,p,r,v,w  ·  src: doc/examples/schematics/cmos-input-model2.sch
W PIO 2;right, size=0.5
W GND 3;right, size=0.5
P PIO GND;down
Rp 2 4;up
Rn 2 3;down
W 2 6;right
Cp 6 5;up
Cn 6 7;down
W 4 5;right
W 3 7;right
VDD 10 9;down, l=V_{DD}
W 8 10; down=0.5
W 5 8;right, size=1.5
W 7 9;right, size=1.5
;draw_nodes=connections, label_ids=False, label_nodes=alpha