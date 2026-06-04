# n2t-id: mutualinductances1  ·  Mutualinductances1
# n2t-tags: cpt:k, cpt:l, cpt:p, cpt:w, curricular:tcii, etiqueta-i, etiqueta-v, magnetico, visibilidad-nodos  ·  cpts: k,l,p,w  ·  src: doc/examples/tutorials/transformers/mutualinductances1.sch
W 1 1a; right, i=i_1
L1 1a 2a; down
W 2 2a; right
K L1 L2 k; right=1.2
W 3 3a; left, i=i_2
L2 3a 4a; down
W 4a 4; right
P1 1 2; down, v_=v_1
P2 3 4; down, v^=v_2
;label_nodes=False, draw_nodes=connections
