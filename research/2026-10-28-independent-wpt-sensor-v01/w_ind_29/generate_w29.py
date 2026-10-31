"""Generate original KiCad W-IND-29 receiver-current MONITOR ONLY.
Not a power safety cut, transmitter, charger, or approved circuit.
"""
from __future__ import annotations
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL
import argparse

PROJECT = 'W29_RX_KELVIN_MONITOR_ONLY'
def uid(name: str) -> str:
    return str(uuid5(NAMESPACE_URL, 'VALDO-W-IND-29/'+name))
def pin(number, name, kind, x, y, orientation):
    return f'''(pin {kind} line (at {x} {y} {orientation}) (length 2.54)
      (name "{name}" (effects (font (size 1.27 1.27))))
      (number "{number}" (effects (font (size 1.27 1.27)))))'''
def lib_symbol(name, ref, value, pins, w=9, h=13, in_bom='yes'):
    short_name=name.split(':')[-1]
    pp='\n'.join(pin(*p) for p in pins)
    return f'''(symbol "{name}" (in_bom {in_bom}) (on_board {in_bom})
      (property "Reference" "{ref}" (at 0 {h+2} 0) (effects (font (size 1.27 1.27))))
      (property "Value" "{value}" (at 0 {-h-2} 0) (effects (font (size 1.27 1.27))))
      (symbol "{short_name}_0_1" (rectangle (start {-w} {h}) (end {w} {-h})
         (stroke (width 0.254) (type default)) (fill (type background))))
      (symbol "{short_name}_1_1" {pp}))'''

# Texas Instruments INA301 SBOS713A, DGK8 pinout; A1 offset 125uV max.
SPECS = {
 'INA301_A1_DGK': ('U', 'INA301A1IDGKR', [
  ('1','VS','power_in',-12.7,10.16,0),
  ('2','OUT','output',12.7,-5.08,180),
  ('3','LIMIT','input',12.7,10.16,180),
  ('4','GND','power_in',-12.7,-10.16,0),
  ('5','RESET','input',12.7,0,180),
  ('6','ALERT_N','open_collector',12.7,5.08,180),
  ('7','IN-','input',-12.7,0,0),
  ('8','IN+','input',-12.7,5.08,0),
 ],9,13,'yes'),
 'SHUNT4_GENERIC': ('R', '0R1_KELVIN_UNQUALIFIED',[
  ('1','POWER_IN','passive',-12.7,5.08,0),
  ('2','POWER_OUT','passive',12.7,5.08,180),
  ('3','SENSE_PLUS','passive',-12.7,-5.08,0),
  ('4','SENSE_MINUS','passive',12.7,-5.08,180),
 ],9,9,'yes'),
 'R': ('R','R',[
  ('1','~','passive',0,5.08,270), ('2','~','passive',0,-5.08,90),
 ],2,2,'yes'),
 'DECLARED_RX5_BENCH': ('J','DECLARED_SOURCE_NOT_REAL',[
  ('1','5V','power_out',10.16,2.54,180),
  ('2','RETURN','power_out',10.16,-2.54,180),
 ],7,7,'no'),
 'DECLARED_RX_LOAD': ('J','DECLARED_LOAD_NOT_REAL',[
  ('1','LOAD5V','passive',-10.16,2.54,0),
  ('2','RETURN','passive',-10.16,-2.54,0),
 ],7,7,'no'),
}
INSTANCES=[
 ('J1','DECLARED_RX5_BENCH',30.48,60.96,'DECLARED_SOURCE_NOT_REAL'),
 ('RSH1','SHUNT4_GENERIC',78.74,68.58,'0R1_KELVIN_UNQUALIFIED'),
 ('U1','INA301_A1_DGK',127,81.28,'INA301A1IDGKR'),
 ('R1','R',165.1,81.28,'8k66'),
 ('R2','R',186.69,81.28,'10k'),
 ('J2','DECLARED_RX_LOAD',226.06,60.96,'DECLARED_LOAD_NOT_REAL'),
]
NETS={
 'RX5_SOURCE':[('J1','1'),('RSH1','1'),('U1','1'),('U1','5'),('R2','1')],
 'GND':[('J1','2'),('J2','2'),('U1','4'),('R1','2')],
 'RX5_LOAD':[('RSH1','2'),('J2','1')],
 'KELVIN_PLUS':[('RSH1','3'),('U1','8')],
 'KELVIN_MINUS':[('RSH1','4'),('U1','7')],
 'LIMIT':[('R1','1'),('U1','3')],
 'ALERT_N_MONITOR_ONLY':[('U1','6'),('R2','2')],
}
def paths():
 return {(ref,number):(round(x+dx,5),round(y-dy,5))
    for ref,typ,x,y,val in INSTANCES
    for number,name,kind,dx,dy,orient in SPECS[typ][2]}
def instance(ref,typ,x,y,value):
 pins=' '.join(f'(pin "{p[0]}" (uuid "{uid(ref+"/pin/"+p[0])}"))' for p in SPECS[typ][2])
 included='yes' if SPECS[typ][-1]=='yes' else 'no'
 return f'''(symbol (lib_id "W29:{typ}") (at {x} {y} 0) (unit 1)
       (in_bom {included}) (on_board {included}) (dnp no) (uuid "{uid(ref)}")
       (property "Reference" "{ref}" (at {x+15} {y-16} 0) (effects (font (size 1.27 1.27))))
       (property "Value" "{value}" (at {x+15} {y-13.5} 0) (effects (font (size 1.27 1.27))))
       {pins}
       (instances (project "{PROJECT}" (path "/{uid('ROOT')}" (reference "{ref}") (unit 1)))))'''
def render_files():
 symbols='\n'.join(lib_symbol(name,*spec) for name,spec in SPECS.items())
 lib=f'(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n{symbols}\n)\n'
 sch_lib='\n'.join(lib_symbol('W29:'+name,*spec) for name,spec in SPECS.items())
 block='\n'.join(instance(*inst) for inst in INSTANCES)
 coords=paths();labels=[]
 for net,pairs in NETS.items():
  for ref,p in pairs:
   x,y=coords[(ref,p)]
   labels.append(f'''(label "{net}" (at {x} {y} 0)
      (effects (font (size 1.27 1.27))) (uuid "{uid('label/'+net+'/'+ref+'/'+p)}"))''')
 x,y=coords[('U1','2')]
 labels.append(f'(no_connect (at {x} {y}) (uuid "{uid("nc-u1-out")}"))')
 warning='(text "RX CURRENT MONITOR ONLY. ALERT_N NOT A POWER CUT. NO TX, FOD, THERMAL OR BROWNOUT PROTECTION." (at 140 34 0) (effects (font (size 1.27 1.27))) (uuid "'+uid('warning')+'"))'
 schematic=f'''(kicad_sch (version 20230121) (generator "valdo-w29-original")
   (uuid "{uid('ROOT')}") (paper "A4")
   (lib_symbols {sch_lib})
   {warning}
   {block}
   {' '.join(labels)}
   (sheet_instances (path "/" (page "1")))
 )\n'''
 table='(sym_lib_table\n (lib (name "W29")(type "KiCad")(uri "'+chr(36)+'{KIPRJMOD}/W29.kicad_sym")(options "")(descr "W29 original RX monitor symbols")))\n'
 return {PROJECT+'.kicad_sch':schematic,'W29.kicad_sym':lib,'sym-lib-table':table}
def main():
 p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');args=p.parse_args()
 root=Path(__file__).resolve().parent
 files=render_files()
 if args.verify:
  errors=[n for n,s in files.items() if not (root/n).is_file() or (root/n).read_text(encoding='utf-8')!=s]
  if errors:raise SystemExit('Generated KiCad assets changed or missing: '+', '.join(errors))
  print('PASS: KiCad files match generator')
 else:
  for n,s in files.items():(root/n).write_text(s,encoding='utf-8')
  print('Generated',', '.join(files))
if __name__=='__main__':main()
