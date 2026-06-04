# n2t-id: tp4-ej09-hemi  ·  Tp4 ej09 hemi
# n2t-tags: cpt:c, cpt:l, cpt:w, curricular-base, curricular:tcii, etiqueta, layout  ·  cpts: c,l,w  ·  src: skill/templates/tp4_ej09_hemi.sch
W in_t 1; right=0.4
L1 1 1a; right=1.5, l^=8\,\mathrm{mH}
C1 1a c; right=1.5, l^=31\,\mathrm{nF}
W c out_t; right=0.6
W c sp; down=0.5
L2 sp t1; down=1.5, offset=-0.45, l_=11{,}1\,\mathrm{mH}
C2 sp t1; down=1.5, offset=0.45, l^=22{,}2\,\mathrm{nF}
L3 t1 t2; down=1.0, l_=14{,}2\,\mathrm{mH}
C3 t2 0; down=1.0, l_=17{,}4\,\mathrm{nF}
W in_b 0; right=3.4
W 0 out_b; right=0.6
