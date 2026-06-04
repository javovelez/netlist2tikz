# n2t-id: simplify-r1c  ·  Simplify R1c
# n2t-tags: cpt:o, cpt:r, cpt:w, curricular:tcii, etiquetas-globales, simplificacion, visibilidad-nodos  ·  cpts: o,r,w  ·  src: doc/examples/netlists/simplify_R1c.sch
Rt1 1 2 {R1 + R2}; right
W 2 3; right
W 3 3a; up=0.5
W 3 3b; down=0.5
O 3a 4a; right
Rt2 3b 4b {1/(1/R5 + 1/R4)}; right
W 4 4a; up=0.5
W 4 4b; down=0.5
R6 4 5; right
; draw_nodes=connections, label_nodes=none, label_ids=none