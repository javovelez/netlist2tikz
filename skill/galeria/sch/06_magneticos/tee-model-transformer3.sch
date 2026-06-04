# n2t-id: tee-model-transformer3  ·  Tee model transformer3
# n2t-tags: cpt:l, cpt:p, cpt:tf, cpt:w, curricular:tcii, etiqueta-i, etiqueta-v, etiquetas-globales, magnetico, visibilidad-nodos  ·  cpts: l,p,tf,w  ·  src: doc/examples/tutorials/transformers/tee-model-transformer3.sch
L1 1 3 {L_1 - M * a}; right, i>^=i_1
L3 3 0_3 {M * a}; down
P1 1 0; down, v_=v_1
W 0 0_3; right
W 0_3 0_4; right
L2 3 6 {L_2 *a**2 - M * a}; right
W 6 4; right=0.5
TF 5 0_5 4 0_4 {1/a}; right
W 5 7; right=0.5, i^<=i_2
W 0_5 0_7; right=0.5
P2 7 0_7; down, v^=v_2
;label_nodes=False, draw_nodes=connections, label_ids=False
