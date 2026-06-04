# n2t-id: sallen-key-lpf2  ·  Sallen key lpf2
# n2t-tags: cpt:c, cpt:e, cpt:p, cpt:r, cpt:w, curricular:tcii, espejo, etiqueta-v, grilla, opamp, visibilidad-nodos  ·  cpts: c,e,p,r,w  ·  src: doc/examples/schematics/sallen-key-lpf2.sch
P 1 0; down, v_=v_{in}(t)
R1 1 2; right
R2 2 3; right
C1 2 4; up
C2 3 9; down
W 4 5; right
W 5 6; right
W 6 7; down=0
W 7 8; right=0.5
E 7 0 opamp 3 11; right, mirror
W 5 11; down=1
P 8 10; down, v=v_{out}(t)
W 0 9; right
W 9 10; right
;draw_nodes=connections, help_lines=1
