# n2t-id: tf-voltage-gain  ·  Tf voltage gain
# n2t-tags: cpt:a, cpt:p, cpt:tp, cpt:v, cpt:w, cuadripolo, curricular:tcii, estilo, etiqueta, etiqueta-v, etiquetas-globales, forma, pines, visibilidad-nodos  ·  cpts: a,p,tp,v,w  ·  src: doc/examples/schematics/tf_voltage_gain.sch
TP 3 4 1 2; right, shape=cloud, l=Independent source free LTI network, fill=blue!10
W 3 m; right=0.5
W 4 n; right=0.5
W i 1; right=0.5
W j 2; right=0.5
A i; l=i, anchor=se
A j; l=j, anchor=ne
A m; l=m, anchor=sw
A n; l=n, anchor=nw
V1 i j Vij; down
P1 i j; down
P2 m n; down, v=V_{mn}
; label_style=value, draw_nodes=connected, label_nodes=node
