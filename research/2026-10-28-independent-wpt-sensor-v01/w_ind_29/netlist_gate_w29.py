"""Strict audit of native KiCad XML for independent RX Kelvin monitor contract.

Original VALDO W29 code. Synthetic fixture tests do not prove real circuits.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from hashlib import sha256
import xml.etree.ElementTree as ET

EXPECTED = {
 '/RX5_SOURCE': {'J1.1','RSH1.1','U1.1','U1.5','R2.1'},
 '/GND': {'J1.2','J2.2','U1.4','R1.2'},
 '/RX5_LOAD': {'RSH1.2','J2.1'},
 '/KELVIN_PLUS': {'RSH1.3','U1.8'},
 '/KELVIN_MINUS': {'RSH1.4','U1.7'},
 '/LIMIT': {'R1.1','U1.3'},
 '/ALERT_N_MONITOR_ONLY': {'U1.6','R2.2'},
 'unconnected-(U1-OUT-Pad2)': {'U1.2'},
}
PARTS={'J1':'DECLARED_SOURCE_NOT_REAL','J2':'DECLARED_LOAD_NOT_REAL',
       'U1':'INA301A1IDGKR','RSH1':'0R1_KELVIN_UNQUALIFIED',
       'R1':'8k66','R2':'10k'}

def audit(xml_bytes: bytes):
 faults=[];actual={};components={};seen=set()
 try:
  r=ET.fromstring(xml_bytes)
  if r.tag!='export':raise ValueError('not a native KiCad export root')
  cs,ns=r.find('components'),r.find('nets')
  if cs is None or ns is None:raise ValueError('components or nets missing')
  for c in cs.findall('comp'):
   ref=c.get('ref');value=c.findtext('value')
   if not ref or value is None or ref in components:raise ValueError('invalid/duplicate component')
   components[ref]=value
  for n in ns.findall('net'):
   name=n.get('name')
   if not name or name in actual:raise ValueError('missing/duplicate net name')
   items=set()
   for x in n.findall('node'):
    ref,p=x.get('ref'),x.get('pin')
    if not ref or not p:raise ValueError('incomplete net node')
    item=f'{ref}.{p}'
    if item in seen:raise ValueError('duplicate or multiply wired pin: '+item)
    seen.add(item);items.add(item)
   actual[name]=items
  if components!=PARTS:faults.append('components differ from frozen electrical review')
  if set(actual)!=set(EXPECTED):
   faults.append('nets added/renamed/omitted: '+str(sorted(set(actual)^set(EXPECTED))))
  for net,wanted in EXPECTED.items():
   if actual.get(net)!=wanted:
    faults.append(f'pin audit failed on {net}: expected {sorted(wanted)}, got {sorted(actual.get(net,[]))}')
  all_wanted=set().union(*EXPECTED.values())
  if seen!=all_wanted:
   faults.append('physical symbol pin coverage differs from contract: '+str(sorted(seen^all_wanted)))
 except (ET.ParseError,TypeError,ValueError) as e:
  faults.append('KiCad export unreadable: '+str(e))
 return {
  'schema':'VALDO-W-IND-29-NATIVE-NETLIST-V1',
  'status':'EXACT_MONITOR_CONNECTIVITY_NO_POWER_APPROVAL' if not faults else 'BLOCKED_NETLIST_MISMATCH',
  'passed':not faults,'faults':faults,'parts':dict(sorted(components.items())),
  'nets':{k:sorted(v) for k,v in sorted(actual.items())},
  'source':'native KiCad-exported XML or explicitly synthetic test input',
  'local_rx_cut_verified':False,'rx_brownout_failoff_verified':False,
  'tx_independent_safety_verified':False,'fod_thermal_emi_verified':False,
  'lithium_connected':False,'physical_power_authorized':False,
 }
def main(argv=None):
 p=argparse.ArgumentParser()
 p.add_argument('xml',type=Path);p.add_argument('--output',type=Path,required=True)
 a=p.parse_args(argv)
 try:
  data=a.xml.read_bytes();result=audit(data)
  result['native_xml_sha256']=sha256(data).hexdigest()
 except OSError as e:
  result=audit(b'');result['faults'].append(str(e))
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 print(result['status'])
 for x in result['faults']:print('BLOCK:',x)
 return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
