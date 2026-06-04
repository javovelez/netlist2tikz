# n2t-id: tp4-ej10-mderiv  ·  Tp4 ej10 mderiv
# n2t-tags: cpt:c, cpt:l, cpt:w, curricular-base, curricular:tcii, etiqueta, layout  ·  cpts: c,l,w  ·  src: skill/templates/tp4_ej10_mderiv.sch
W in_t 1; right=0.5
L1 1 m1; right=2, offset=0.35, l^=5{,}3\,\mathrm{mH}
C1 1 m1; right=2, offset=-0.35, l_=1.380\,\mathrm{nF}
W m1 c; right=0.45
W c m2; right=0.45
L2 m2 3; right=2, offset=0.35, l^=5{,}3\,\mathrm{mH}
C2 m2 3; right=2, offset=-0.35, l_=1.380\,\mathrm{nF}
W 3 out_t; right=0.5
L3 c 4; down=1.1, l_=3{,}9\,\mathrm{mH}
C3 4 5; down=1.1, l_=1.860\,\mathrm{nF}
L4 5 6; down=1.6, offset=-0.55, l_=4{,}3\,\mathrm{mH}
C4 5 6; down=1.6, offset=0.55, l^=1.680\,\mathrm{nF}
W 6 0; down=0.5
W in_b 0; right=3.4
W 0 out_b; right=3.4
