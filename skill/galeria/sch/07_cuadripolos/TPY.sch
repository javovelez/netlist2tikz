# n2t-id: tpy  ·  TPY
# n2t-tags: cpt:i, cpt:p, cpt:tp, cpt:w, cuadripolo, curricular:tcii, etiqueta, etiqueta-i, etiqueta-v, visibilidad-nodos  ·  cpts: i,p,tp,w  ·  src: doc/examples/schematics/TPY.sch
P 1 2; down, v_=V_1
W 1 11; right=0.75, i=I_1
W 2 12; right=0.75, i<=I_1
I1y 12 11; up
W 11 5; right=0.25
W 12 6; right=0.25
TPY 7 8 5 6; right, l={Source-free Y-parameters two-port}
W 7 9; right=0.25
W 8 10; right=0.25
I2y 10 9; up
W 9 3; right=0.5, i=I_2
W 10 4; right=0.5, i<=I_2
P 3 4; down, v^=V_2
; label_nodes=none, draw_nodes=connections
