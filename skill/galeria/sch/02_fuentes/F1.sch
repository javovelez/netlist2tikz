# n2t-id: f1  ·  F1
# n2t-tags: cpt:c, cpt:f, cpt:p, cpt:r, cpt:v, cpt:w, curricular:tcii, etiqueta, etiqueta-v, etiquetas-globales, fuente, visibilidad-nodos  ·  cpts: c,f,p,r,v,w  ·  src: doc/examples/schematics/F1.sch
V1 1 0_1; down
R1 1 2 R_s; right=1.5
C1 2 0; down, v=v_C
W 0_1 0; right
W 0 0_2; right
R2 2_2 0_2 R_in; down, v=v_{in}
W 2 2_2; right
F1 3 0_3 V1 F; down, l=F i_{in}
R3 3 4 R_out; right=1.5
R4 4 0_4 R_L; down
W 0_2 0_3; size=1.2
W 0_3 0_4
P1 4 0_4; down
; label_ids=False, draw_nodes=connections, label_nodes=False