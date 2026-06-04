# n2t-id: cmos-r-series-c-load-thevenin  ·  Cmos R series C load thevenin
# n2t-tags: cpt:c, cpt:p, cpt:r, cpt:u, cpt:v, cpt:w, estilo, etiqueta, etiqueta-i, etiqueta-v, transistor, visibilidad-nodos  ·  cpts: c,p,r,u,v,w  ·  src: doc/examples/tutorials/nonlinear/cmos_R_series_C_load_thevenin.sch
U1 inverter; right, fill=blue!50, l
W U1.vss 0; down
W U1.out 1; right=0.5, i=I_o
W 0 0_1; right=0.5
P 1 0_1; down, v=V_o
Rs 1 1_1; right=2
Cl 1_1 0_2; down, v=V_l
W 0_1 0_2; right
Rt 1_1 1_2; right=2
Vt 1_2 0_3; down=1.5
W 0_2 0_3; right
; draw_nodes=connections, label_nodes=none
