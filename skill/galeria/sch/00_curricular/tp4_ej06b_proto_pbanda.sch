# n2t-id: tp4-ej06b-proto-pbanda  ·  Tp4 ej06b proto pbanda
# n2t-tags: cpt:c, cpt:l, cpt:w, curricular-base, curricular:tcii, etiqueta, layout  ·  cpts: c,l,w  ·  src: skill/templates/tp4_ej06b_proto_pbanda.sch
W in_t 1; right=0.4
L1 1 1a; right=1.6, l^=\frac{L_1}{2}
C1 1a m1; right=1.6, l^=\frac{2}{\omega_0^2 L_1}
W m1 c; right=0.4
W c m2; right=0.4
C1b m2 2c; right=1.6, l^=\frac{2}{\omega_0^2 L_1}
L1b 2c 3; right=1.6, l=\frac{L_1}{2}
W 3 out_t; right=0.4
W c sp; down=0.6
L2 sp 5; down=1.8, offset=-0.5, l_=\frac{1}{\omega_0^2 C_2}
C2 sp 5; down=1.8, offset=0.5, l^=C_2
W 5 0; down=0.5
W in_b 0; right=4.0
W 0 out_b; right=4.0
