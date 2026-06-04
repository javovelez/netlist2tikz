# n2t-id: transfer1  ·  Transfer1
# n2t-tags: analisis, cpt:p, cpt:r, cpt:w, curricular:tcii, etiqueta-i, etiqueta-v, visibilidad-nodos  ·  cpts: p,r,w  ·  src: doc/examples/netlists/transfer1.sch
P1 1 0; down, v_=V_1
R1 1 2; right=2, i>^=I_1
R2 2 0_2; down=1.5
R3 2 3; right=2, i^<=I_2
W 0 0_2; right
P2 3 0_3; down, v=V_2
W 0_2 0_3; right
; draw_nodes=connections, label_nodes=primary
