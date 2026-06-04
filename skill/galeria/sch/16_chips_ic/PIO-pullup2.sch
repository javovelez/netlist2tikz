# n2t-id: pio-pullup2  ·  PIO pullup2
# n2t-tags: chip, cpt:m, cpt:r, cpt:u, cpt:w, espejo, estilo, etiqueta, pad-senal, pines, tierra, visibilidad-nodos  ·  cpts: m,r,u,w  ·  src: doc/examples/schematics/digital/PIO-pullup2.sch
W 3 3a; up=0.1, rground, l=VDDIO
M1 1 2 3 pmos; right, l={}
R 1 4; down, l={}
W 4 5; right=0.5, bidir, l=PA0, fill=purple!50
U2 buffer; right, fliplr, l={}, fill=red!50
W U2.in 4; right=1
U1 dff; right=1, pinlabels={q,d,clk}, fill=green!50, l={}
W U1.q 2; right=0.01
; label_nodes=none, draw_nodes=connections
