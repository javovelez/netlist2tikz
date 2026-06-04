# n2t-id: opamp-differential-amplifier1  ·  Opamp differential amplifier1
# n2t-tags: cpt:e, cpt:p, cpt:r, cpt:w, curricular:tcii, espejo, opamp, visibilidad-nodos  ·  cpts: e,p,r,w  ·  src: doc/examples/schematics/opamp-differential-amplifier1.sch
P1 1 0_1; down
P2 4 0_1; down
R1 1 2; right
R2 2_1 3_1; right
E1 3_2 0_3 opamp 2_0 2 A; mirror
W 0_1 0; right
R3 4 2_0; right
R4 2_0 0; down=1.5
W 3_2 3; right
W 0 0_3; right
P3 3 0_3; down
W 2_1 2; down
W 3_1 3_2; down
;draw_nodes=connections
