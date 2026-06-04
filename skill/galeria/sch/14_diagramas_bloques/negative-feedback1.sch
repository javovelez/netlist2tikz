# n2t-id: negative-feedback1  ·  Negative feedback1
# n2t-tags: cpt:shape, cpt:sp, cpt:w, curricular:senales, diagrama-bloques, etiqueta, forma, layout, visibilidad-nodos  ·  cpts: shape,sp,w  ·  src: doc/examples/schematics/negative-feedback1.sch
W 1 SP1._1; right=0.5, endarrow=tri
SP1 pm ._1 ._2 ._3; right=1, l={}
W SP1._3 S1.w; endarrow=tri
S1 box; right=1.5, aspect=1.5, l=Open-loop gain (A)
W S1.e 2; right
W 2 3; down
S2 box; right=1.5, aspect=1.5, l=Attenuator $\beta$
W 3 S2.e; left, endarrow=tri
W S2.w 4; left
W 4 SP1._2; up, endarrow=tri
W 2 5; right=0.5, endarrow=tri
; draw_nodes=false, label_nodes=false