# n2t-id: txline1  ·  Txline1
# n2t-tags: cpt:p, cpt:r, cpt:tl, cpt:v, cpt:w, etiqueta, etiqueta-v, linea-transmision, visibilidad-nodos  ·  cpts: p,r,tl,v,w  ·  src: doc/examples/tutorials/txline/txline1.sch
Vs 1 0 step; down
Rs 1 2a; right
W 2a 2; right=0.5
TL 3 0_3 2 0_2 lossless; right, l=Z_0
W 3 4; right=0.5
Rl 4 0_4; down
W 0_3 0_4; right
W 0 0_2; right
P2 3 0_3; down, v=V_2
P1 2 0_2; down, v_=V_1
; draw_nodes=connections, label_nodes=none
