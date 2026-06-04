# n2t-id: ic3  ·  Ic3
# n2t-tags: chip, cpt:u, cpt:w, etiqueta, etiquetas-globales, forma, grilla, pines, tierra  ·  cpts: u,w  ·  src: doc/examples/schematics/ic3.sch
U1 regulator; right, aspect=1.33333333, pinnames={en}
W U1.out 2; right=0.5
W 3 U1.in; right=0.5
W 2 3V3; implicit, up=0.4, l=3V3
W U1.gnd GND; implicit, down=0.2, l=GND
; draw_labels=connections, help_lines=1
