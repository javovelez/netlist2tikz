# n2t-id: simplify-r1b  ·  Simplify R1b
# n2t-tags: cpt:r, cpt:w, curricular:tcii, etiquetas-globales, simplificacion, visibilidad-nodos  ·  cpts: r,w  ·  src: doc/examples/netlists/simplify_R1b.sch
Rt1 1 2 {R1 + R2}; right
W 2 3; right
W 3 3a; up=0.5
W 3 3b; down=0.5
R4 3a 4a; right
R5 3b 4b; right
W 4 4a; up=0.5
W 4 4b; down=0.5
R6 4 5; right
; draw_nodes=connections, label_nodes=none, label_ids=none