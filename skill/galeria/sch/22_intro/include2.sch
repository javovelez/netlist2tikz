# n2t-id: include2  ·  Include2
# n2t-tags: cpt:w, curricular:tcii, intro, visibilidad-nodos  ·  cpts: w  ·  src: doc/examples/schematics/include2.sch
.include LC1.sch as s1
.include LC1.sch as s2
.include LC1.sch as s3
.include LC1.sch as s4
W s1.2 s2.1; right=0.1
W s1.3 s2.0; right=0.1
W s2.2 s3.1; right=0.1
W s2.3 s3.0; right=0.1
W s3.2 s4.1; right=0.1
W s3.3 s4.0; right=0.1
; draw_nodes=connections