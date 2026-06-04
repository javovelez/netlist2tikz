# n2t-id: tp4-ej09-mderiv  ·  Tp4 ej09 mderiv
# n2t-tags: cpt:c, cpt:l, cpt:w, curricular-base, curricular:tcii, etiqueta, layout  ·  cpts: c,l,w  ·  src: skill/templates/tp4_ej09_mderiv.sch
W in_t 1; right=0.4
L1 1 1a; right=1.5, l^=10\,\mathrm{mH}
C1 1a m1; right=1.5, l^=24{,}5\,\mathrm{nF}
W m1 c; right=0.4
W c m2; right=0.4
C1b m2 2c; right=1.5, l^=24{,}5\,\mathrm{nF}
L1b 2c 3; right=1.5, l=10\,\mathrm{mH}
W 3 out_t; right=0.4
W c sp; down=0.5
L2 sp t1; down=1.5, offset=-0.45, l_=4{,}4\,\mathrm{mH}
C2 sp t1; down=1.5, offset=0.45, l^=56\,\mathrm{nF}
L3 t1 t2; down=1.0, l_=3{,}8\,\mathrm{mH}
C3 t2 0; down=1.0, l_=65\,\mathrm{nF}
W in_b 0; right=3.8
W 0 out_b; right=3.8
