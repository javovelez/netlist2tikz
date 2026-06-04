# n2t-id: ss2  ·  Ss2
# n2t-tags: analisis, cpt:c, cpt:l, cpt:r, cpt:v, cpt:w, curricular:tcii, etiqueta-i, etiqueta-v  ·  cpts: c,l,r,v,w  ·  src: doc/examples/netlists/ss2.sch
V 1 0 {v(t)}; down
R1 1 2; right
L 2 3; right=1.5, i={i_L}
R2 3 0_3; down=1.5, i={i_{R2}}, v={v_{R2}}
W 0 0_3; right
W 3 3_a; right
C 3_a 4; down, i={i_C}, v={v_C}
R3 4 0_4; down
W 0_3 0_4; right
