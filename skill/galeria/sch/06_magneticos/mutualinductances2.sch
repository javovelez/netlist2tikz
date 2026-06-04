# n2t-id: mutualinductances2  ·  Mutualinductances2
# n2t-tags: cpt:k, cpt:l, cpt:p, cpt:w, curricular:tcii, etiqueta-i, etiqueta-v, magnetico, visibilidad-nodos  ·  cpts: k,l,p,w  ·  src: doc/examples/tutorials/transformers/mutualinductances2.sch
W 1 1a; right, i>^=i_1
L1 1a 2a; down
W 2 2a; right
K L1 L2 k; right=1.2
W 3 3a; left, i_>=i_2
L2 3a 4a; down
W 4a 4; right
P1 1 2; down, v_=v_1
P2 3 4; down, v^=v_2
W 2a 4a; right
;label_nodes=False, draw_nodes=connections
