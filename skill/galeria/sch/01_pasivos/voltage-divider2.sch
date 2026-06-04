# n2t-id: voltage-divider2  ·  Divisor de tensión (variante)
# n2t-tags: cpt:p, cpt:r, cpt:v, cpt:w, curricular:tcii, estilo-simbolo, etiqueta-v, geometria-global, pasivo, visibilidad-nodos  ·  cpts: p,r,v,w  ·  src: doc/examples/schematics/voltage-divider2.sch
Vi 1 0_1; down=1.5
R1 1 2; right=1.5
R2 2 0; down
P1 2_2 0_2; down, v=V_o
W 2 2_2; right
W 0_1 0; right
W 0 0_2; right
; draw_nodes=connections, node_spacing=3, scale=0.5, style=european, bipole label style={color=blue}
