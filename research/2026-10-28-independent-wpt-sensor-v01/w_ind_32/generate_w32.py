"""W-IND-32: original, editable KiCad 9 schematic of an INCOMPLETE RX gate.

NOT a certified safety cutoff. Permits are unimplemented external inputs;
FOD, thermal, supervisor and local-rearm hardware remain absent.
"""
from __future__ import annotations
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL
import argparse

PROJECT = 'W32_RX_DUAL_RCB_INCOMPLETE'
PREFIX = 'W32'

def uid(key):
    return str(uuid5(NAMESPACE_URL, 'valdo-original-w32/'+key))

def p(n, title, kind, x, y, direction):
    return (str(n), title, kind, x, y, direction)

# RPW pin map is for the 470x variant ONLY; 472x/474x differ on pins 2-4.
# Datasheet TI TPS25947, Rev C, pin configuration / functions.
SPECS = {
 'SOURCE': ('J', 'DECLARED_BENCH_5V_NOT_REAL', [p(1,'5V','power_out',10.16,2.54,180),p(2,'RTN','power_out',10.16,-2.54,180)],7,7,False),
 'LOAD': ('J', 'DECLARED_RESISTOR_LOAD_NOT_REAL', [p(1,'IN','passive',-10.16,2.54,0),p(2,'RTN','passive',-10.16,-2.54,0)],7,7,False),
 'PERMIT': ('J', 'EXTERNAL_PERMIT_DRIVER_NOT_BUILT', [p(1,'PERMIT','passive',10.16,2.54,180),p(2,'GND','passive',10.16,-2.54,180)],7,7,False),
 'SHUNT': ('R', '0R1_4WIRE_TBD', [p(1,'PWR_IN','passive',-12.7,5.08,0),p(2,'PWR_OUT','passive',12.7,5.08,180),p(3,'K_PLUS','passive',-12.7,-5.08,0),p(4,'K_MINUS','passive',12.7,-5.08,180)],9,9,True),
 'INA301A1_DGK': ('U','INA301A1IDGKR', [p(1,'VS','power_in',-12.7,10.16,0),p(2,'OUT','output',12.7,-5.08,180),p(3,'LIMIT','input',12.7,10.16,180),p(4,'GND','power_in',-12.7,-10.16,0),p(5,'RESET','input',12.7,0,180),p(6,'ALERT_N','open_collector',12.7,5.08,180),p(7,'IN-','input',-12.7,0,0),p(8,'IN+','input',-12.7,5.08,0)],9,13,True),
 'TPS259470_RPW10': ('U','TPS259470LRPWR', [
    p(1,'EN/UVLO','input',-12.7,10.16,0),p(2,'OVLO','input',-12.7,5.08,0),
    p(3,'AUXOFF','open_collector',12.7,10.16,180),p(4,'FLT_N','open_collector',12.7,5.08,180),
    p(5,'IN','passive',-12.7,0,0),p(6,'OUT','passive',12.7,0,180),
    p(7,'DVDT','passive',12.7,-5.08,180),p(8,'GND','power_in',-12.7,-10.16,0),
    p(9,'ILM','passive',12.7,-10.16,180),p(10,'ITIMER','passive',12.7,-15.24,180)
 ],9,18,True),
 'R': ('R','R',[p(1,'~','passive',0,5.08,270),p(2,'~','passive',0,-5.08,90)],2,2,True),
 'C': ('C','C',[p(1,'~','passive',0,5.08,270),p(2,'~','passive',0,-5.08,90)],2,2,True),
}

INSTANCES = [
 ('J1','SOURCE',22.86,87.63,'DECLARED_BENCH_5V_NOT_REAL'),
 ('J2','LOAD',228.6,87.63,'DECLARED_RESISTOR_LOAD_NOT_REAL'),
 ('RSH1','SHUNT',68.58,105.41,'0R1_4WIRE_TBD'),
 ('U1','INA301A1_DGK',100.33,52.07,'INA301A1IDGKR'),
 ('R1','R',139.7,52.07,'8k66'),('R2','R',160.02,52.07,'10k'),
 ('C1','C',180.34,52.07,'100nF_DECOUPLE_TBD'),
 ('U2','TPS259470_RPW10',116.84,111.76,'TPS259470LRPWR'),
 ('U3','TPS259470_RPW10',177.8,111.76,'TPS259470LRPWR'),
 ('J3','PERMIT',22.86,156.21,'PERMIT_A_EXTERNAL_UNQUALIFIED'),
 ('J4','PERMIT',22.86,182.88,'PERMIT_B_EXTERNAL_UNQUALIFIED'),
 ('RPD1','R',68.58,161.29,'10k_PULLDOWN_A'),('RPD2','R',121.92,161.29,'10k_PULLDOWN_B'),
 ('RILM1','R',147.32,149.86,'RILM_A_TBD'),('RILM2','R',195.58,149.86,'RILM_B_TBD'),
 ('CIT1','C',147.32,177.8,'CIT_A_TBD'),('CIT2','C',195.58,177.8,'CIT_B_TBD'),
]

NETS = {
 'RX5_SOURCE':[('J1','1'),('RSH1','1'),('U1','1'),('U1','5'),('R2','1'),('C1','1')],
 'GND':[('J1','2'),('J2','2'),('J3','2'),('J4','2'),('U1','4'),('U2','8'),('U3','8'),('R1','2'),('C1','2'),('RPD1','2'),('RPD2','2'),('RILM1','2'),('RILM2','2'),('CIT1','2'),('CIT2','2'),('U2','2'),('U3','2')],
 'RX5_POST_SHUNT':[('RSH1','2'),('U2','5')],
 'RX5_BETWEEN_CUTS':[('U2','6'),('U3','5')],
 'RX5_LOAD':[('U3','6'),('J2','1')],
 'KELVIN_PLUS':[('RSH1','3'),('U1','8')],
 'KELVIN_MINUS':[('RSH1','4'),('U1','7')],
 'LIMIT':[('R1','1'),('U1','3')],
 'ALERT_N_READ_ONLY':[('U1','6'),('R2','2')],
 'PERMIT_A_UNQUALIFIED':[('J3','1'),('RPD1','1'),('U2','1')],
 'PERMIT_B_UNQUALIFIED':[('J4','1'),('RPD2','1'),('U3','1')],
 'ILM_A':[('U2','9'),('RILM1','1')],
 'ILM_B':[('U3','9'),('RILM2','1')],
 'ITIMER_A':[('U2','10'),('CIT1','1')],
 'ITIMER_B':[('U3','10'),('CIT2','1')],
}
NC = [('U1','2'),('U2','3'),('U2','4'),('U2','7'),('U3','3'),('U3','4'),('U3','7')]

def pin_symbol(number,name,kind,x,y,orient):
    return f'''(pin {kind} line (at {x} {y} {orient}) (length 2.54)
       (name "{name}" (effects (font (size 1.27 1.27))))
       (number "{number}" (effects (font (size 1.27 1.27)))))'''

def lib_symbol(name,spec):
    ref, val, pins, w, h, included = spec
    leaf = name.rsplit(':',1)[-1]
    ps='\n'.join(pin_symbol(*x) for x in pins)
    return f'''(symbol "{name}" (in_bom {'yes' if included else 'no'}) (on_board {'yes' if included else 'no'})
      (property "Reference" "{ref}" (at 0 {h+2} 0) (effects (font (size 1.27 1.27))))
      (property "Value" "{val}" (at 0 {-h-2} 0) (effects (font (size 1.27 1.27))))
      (symbol "{leaf}_0_1" (rectangle (start {-w} {h}) (end {w} {-h})
       (stroke (width 0.254) (type default)) (fill (type background))))
      (symbol "{leaf}_1_1" {ps}))'''

def coordinates():
    return {(ref,pin[0]):(round(x+pin[3],5),round(y-pin[4],5))
            for ref,typ,x,y,_ in INSTANCES for pin in SPECS[typ][2]}

def instance(ref,typ,x,y,val):
    used='yes' if SPECS[typ][-1] else 'no'
    pins='\n'.join(f'(pin "{p[0]}" (uuid "{uid(ref+"/pin/"+p[0])}"))' for p in SPECS[typ][2])
    return f'''(symbol (lib_id "{PREFIX}:{typ}") (at {x} {y} 0) (unit 1)
     (in_bom {used}) (on_board {used}) (dnp no) (uuid "{uid(ref)}")
     (property "Reference" "{ref}" (at {x+15} {y-21} 0) (effects (font (size 1.27 1.27))))
     (property "Value" "{val}" (at {x+15} {y-18.5} 0) (effects (font (size 1.27 1.27))))
     {pins}
     (instances (project "{PROJECT}" (path "/{uid('ROOT')}" (reference "{ref}") (unit 1)))))'''

def render_files():
    lib='\n'.join(lib_symbol(n,s) for n,s in SPECS.items())
    lib_all='\n'.join(lib_symbol(PREFIX+':'+n,s) for n,s in SPECS.items())
    coords=coordinates()
    labels=[]
    for net,nodes in NETS.items():
        for ref,num in nodes:
            x,y=coords[(ref,num)]
            labels.append(f'(label "{net}" (at {x} {y} 0) (effects (font (size 1.27 1.27))) (uuid "{uid("label/"+net+"/"+ref+"/"+num)}"))')
    for ref,num in NC:
        x,y=coords[(ref,num)]
        labels.append(f'(no_connect (at {x} {y}) (uuid "{uid("NC/"+ref+"/"+num)}"))')
    warnings=[
     'INCOMPLETE RX CUT TOPOLOGY - DO NOT FABRICATE / ENERGIZE.',
     'TWO TPS259470L STAGES; EXTERNAL PERMITS NOT QUALIFIED; PULL-DOWNS ONLY.',
     'INA301 ALERT IS READ-ONLY, NOT CONNECTED TO EN. NO FOD/THERMAL/POR/REARM HARDWARE.',
     'ILM / ITIMER ARE TBD; OVLO IS GROUNDED AND THUS NO OVP; DVDT OPEN (INRUSH UNSIZED).',
     'NO TX, NO DOCK, NO BATTERY/BMS, NO EMI OR PHYSICAL DATA.'
    ]
    notes='\n'.join(f'(text "{msg}" (at 145 {14+i*6} 0) (effects (font (size 1.27 1.27))) (uuid "{uid("note/"+str(i))}"))' for i,msg in enumerate(warnings))
    schematic=f'''(kicad_sch (version 20230121) (generator "valdo-w32-original")
      (uuid "{uid('ROOT')}") (paper "A3")
      (lib_symbols {lib_all})
      {notes}
      {' '.join(instance(*inst) for inst in INSTANCES)}
      {' '.join(labels)}
      (sheet_instances (path "/" (page "1")))
    )\n'''
    symtab='(sym_lib_table\n  (lib (name "W32")(type "KiCad")(uri "'+chr(36)+'{KIPRJMOD}/W32.kicad_sym")(options "")(descr "Original W32, NOT qualified")))\n'
    return {PROJECT+'.kicad_sch':schematic,
            'W32.kicad_sym':f'(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n{lib}\n)\n',
            'sym-lib-table':symtab}

def main():
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');args=p.parse_args()
    root=Path(__file__).parent;files=render_files()
    if args.verify:
        diff=[n for n,c in files.items() if not (root/n).exists() or (root/n).read_text()!=c]
        if diff:raise SystemExit('BLOCKED changed/missing generated assets: '+', '.join(diff))
        print('PASS: generator assets reproducible')
    else:
        for n,c in files.items():(root/n).write_text(c)
        print('Generated:',', '.join(files))
if __name__=='__main__': main()
