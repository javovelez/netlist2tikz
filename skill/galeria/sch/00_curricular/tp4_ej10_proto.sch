# n2t-id: tp4-ej10-proto  ·  Tp4 ej10 proto
# n2t-tags: cpt:c, cpt:l, cpt:w, curricular-base, curricular:tcii, etiqueta, layout  ·  cpts: c,l,w  ·  src: skill/templates/tp4_ej10_proto.sch
W in_t 1; right=0.5
L1 1 m1; right=2, offset=0.35, l^=8{,}5\,\mathrm{mH}
C1 1 m1; right=2, offset=-0.35, l_=849\,\mathrm{nF}
W m1 c; right=0.45
W c m2; right=0.45
L2 m2 3; right=2, offset=0.35, l^=8{,}5\,\mathrm{mH}
C2 m2 3; right=2, offset=-0.35, l_=849\,\mathrm{nF}
W 3 out_t; right=0.5
L3 c 4; down=1.2, l_=2{,}4\,\mathrm{mH}
C3 4 0; down=1.2, l_=3.030\,\mathrm{nF}
W in_b 0; right=3.4
W 0 out_b; right=3.4
