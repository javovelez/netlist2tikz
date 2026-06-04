# n2t-id: blocks2  ·  Blocks2
# n2t-tags: cpt:bl, curricular:senales, diagrama-bloques, etiqueta, kind, kind:adc, kind:dac, kind:dsp, kind:fft, kind:phaseshifter, kind:piattenuator, kind:tattenuator, kind:twoport, kind:vphaseshifter, kind:vpiattenuator, kind:vtattenuator, visibilidad-nodos  ·  cpts: bl  ·  src: doc/examples/schematics/blocks2.sch
BL1 1 2; right, kind=adc, l=adc
BL2 2 3; right, kind=dac, l=dac
BL3 3 4; right, kind=piattenuator, l=piattenuator
BL4 4 5; right, kind=vpiattenuator, l=vpiattenuator
BL5 5 6; right, kind=tattenuator, l=tattenuator
BL6 6 7; right, kind=vtattenuator, l=vtattenuator
BL7 7 8; right, kind=phaseshifter, l=phaseshifter
BL8 8 9; right, kind=vphaseshifter, l=vphaseshifter
BL9 9 10; right, kind=dsp, l=dsp
BL10 10 11; right, kind=fft, l=fft
BL11 11 12; right, kind=twoport, l=twoport
; label_nodes=false, draw_nodes=connections
