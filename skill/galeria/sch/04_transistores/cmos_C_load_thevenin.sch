# n2t-id: cmos-c-load-thevenin  ·  Cmos C load thevenin
# n2t-tags: cpt:c, cpt:p, cpt:r, cpt:u, cpt:v, cpt:w, estilo, etiqueta, etiqueta-i, etiqueta-v, transistor, visibilidad-nodos  ·  cpts: c,p,r,u,v,w  ·  src: doc/examples/tutorials/nonlinear/cmos_C_load_thevenin.sch
U1 inverter; right, fill=blue!50, l
W U1.vss 0; down, color=blue
W U1.out 1; right=0.5, color=blue, i=I_o
W 0 0_1; right=0.5, color=blue
P 1 0_1; down, v=V_o
W 1 1_1; right
Cl 1_1 0_2; down, v=V_l
W 0_1 0_2; right
Rt 1_1 1_2; right=2
Vt 1_2 0_3; down
W 0_2 0_3; right
; draw_nodes=connections, label_nodes=none, color=blue
