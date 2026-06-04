# n2t-id: shunt  ·  Shunt
# n2t-tags: cpt:p, cpt:w, cpt:z, curricular:tcii, etiqueta, etiqueta-i, etiqueta-v, red, visibilidad-nodos  ·  cpts: p,w,z  ·  src: doc/examples/schematics/shunt.sch
P1 1 0; down, v_=V_1
W 1 2; right, i=I_1
W 0 0_2; right
Z 2 0_2; down, l=OP
W 3 2; left, i=I_2
W 0_2 0_3; right
P2 3 0_3; down, v^=V_2
;label_nodes=False, draw_nodes=connections
