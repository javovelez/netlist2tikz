# n2t-id: twoport1  ·  Cuadripolo genérico (caja)
# n2t-tags: cpt:p, cpt:tp, cpt:w, cuadripolo, curricular:tcii, etiqueta, etiqueta-i, etiqueta-v, visibilidad-nodos  ·  cpts: p,tp,w  ·  src: doc/examples/schematics/twoport1.sch
TP1 1 2 3 4; right, l=Two-port network
W 1 1a; right=0.5, i^<=I_2
W 2 2a; right=0.5, i_=I_2
W 3a 3; right=0.5, i=I_1
W 4a 4; right=0.5, ir=I_1
P 1a 2a; down, v^=V_2
P 3a 4a; down, v_=V_1
; draw_nodes=none, label_nodes=none
