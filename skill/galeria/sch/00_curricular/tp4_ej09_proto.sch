# n2t-id: tp4-ej09-proto  ·  Tp4 ej09 proto
# n2t-tags: cpt:c, cpt:l, cpt:w, curricular-base, curricular:tcii, etiqueta, layout  ·  cpts: c,l,w  ·  src: skill/templates/tp4_ej09_proto.sch
W in_t 1; right=0.4
L1 1 1a; right=1.5, l^=13\,\mathrm{mH}
C1 1a m1; right=1.5, l^=18{,}5\,\mathrm{nF}
W m1 c; right=0.4
W c m2; right=0.4
C1b m2 2c; right=1.5, l^=18{,}5\,\mathrm{nF}
L1b 2c 3; right=1.5, l=13\,\mathrm{mH}
W 3 out_t; right=0.4
W c sp; down=0.5
L2 sp 5; down=1.6, offset=-0.45, l_=3{,}3\,\mathrm{mH}
C2 sp 5; down=1.6, offset=0.45, l^=74\,\mathrm{nF}
W 5 0; down=0.5
W in_b 0; right=3.8
W 0 out_b; right=3.8
