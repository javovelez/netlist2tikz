# n2t-id: cmos-led-model1  ·  Cmos led model1
# n2t-tags: cmos, cpt:d, cpt:p, cpt:r, cpt:v, cpt:w, etiqueta, etiqueta-i, etiqueta-v, visibilidad-nodos  ·  cpts: d,p,r,v,w  ·  src: doc/examples/schematics/cmos-led-model1.sch
VDD 7 0_3; down=1.5
Ro 7 1; right=2, l=R_o(I_o)
R 1 2; right=2, i>^=I_o
D 2 0_2 led; down, v=V_f, l={}
W 0_3 0_1; right
W 0_1 0_2; right
P 1 0_1; down, v=V_o
; draw_nodes=connections, label_nodes=false