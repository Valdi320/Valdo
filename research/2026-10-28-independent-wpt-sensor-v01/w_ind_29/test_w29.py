"""Original deterministic synthetic netlist mutation tests for W-IND-29.

Real KiCad export is validated separately in CI; tests cannot approve power.
"""
import copy
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import generate_w29 as gen
from netlist_gate_w29 import EXPECTED,PARTS,audit,main

def sample():
 r=ET.Element('export');c=ET.SubElement(r,'components');ns=ET.SubElement(r,'nets')
 for ref,v in PARTS.items():
  cc=ET.SubElement(c,'comp',ref=ref);ET.SubElement(cc,'value').text=v
 for i,(name,parts) in enumerate(EXPECTED.items()):
  net=ET.SubElement(ns,'net',name=name,code=str(i+1))
  for spec in sorted(parts):
   ref,p=spec.rsplit('.',1);ET.SubElement(net,'node',ref=ref,pin=p)
 return r
def encoded(root):return ET.tostring(root,encoding='utf-8')
def net(root,name):return next(x for x in root.find('nets') if x.get('name')==name)

class W29Generator(unittest.TestCase):
 def test_stable_uuids(self):self.assertEqual(gen.uid('U1'),gen.uid('U1'))
 def test_unique_uuids(self):self.assertEqual(len({gen.uid(x) for x in ('U1','U2','R1')}),3)
 def test_every_pin_has_a_coordinate(self):
  expected={(r,p[0]) for r,s,*_ in gen.INSTANCES for p in gen.SPECS[s][2]}
  self.assertEqual(set(gen.paths()),expected)
 def test_no_duplicate_component_pin_contract(self):
  pins=[pair for pairs in gen.NETS.values() for pair in pairs]
  self.assertEqual(len(pins),len(set(pins)))
 def test_only_explicit_monitor_nc(self):
  unused=set(gen.paths())-{pair for pairs in gen.NETS.values() for pair in pairs}
  self.assertEqual(unused,{('U1','2')})
 def test_receiver_and_source_are_separate(self):
  self.assertNotEqual(gen.NETS['RX5_SOURCE'],gen.NETS['RX5_LOAD'])
  self.assertNotIn(('U1','6'),gen.NETS['RX5_SOURCE'])
 def test_kplus_kminus_are_distinct(self):
  self.assertEqual(gen.NETS['KELVIN_PLUS'],[('RSH1','3'),('U1','8')])
  self.assertEqual(gen.NETS['KELVIN_MINUS'],[('RSH1','4'),('U1','7')])
 def test_ti_verified_pin_mapping(self):
  m={p[0]:p[1] for p in gen.SPECS['INA301_A1_DGK'][2]}
  self.assertEqual(m,{'1':'VS','2':'OUT','3':'LIMIT','4':'GND','5':'RESET','6':'ALERT_N','7':'IN-','8':'IN+'})
 def test_generated_file_matches(self):
  for path,data in gen.render_files().items():
   self.assertEqual((Path(__file__).resolve().parent/path).read_text(encoding='utf-8'),data)

class W29XMLGuard(unittest.TestCase):
 def setUp(self):self.r=sample()
 def checkbad(self):
  x=audit(encoded(self.r));self.assertFalse(x['passed'],x)
  self.assertFalse(x['physical_power_authorized']);return x
 def test_synthetic_fixture_accepts_as_topology_only(self):
  x=audit(encoded(self.r));self.assertTrue(x['passed']);self.assertFalse(x['local_rx_cut_verified'])
 def test_wrong_ina_input_polarity(self):
  n=net(self.r,'/KELVIN_PLUS');n.find('node[@ref="U1"]').set('pin','7');self.checkbad()
 def test_shunt_sense_swap(self):
  n=net(self.r,'/KELVIN_MINUS');n.find('node[@ref="RSH1"]').set('pin','3');self.checkbad()
 def test_short_kelvin_plus_minus(self):
  minus=net(self.r,'/KELVIN_MINUS');plus=net(self.r,'/KELVIN_PLUS')
  for x in list(minus):plus.append(copy.deepcopy(x))
  self.r.find('nets').remove(minus);self.checkbad()
 def test_short_power_in_out(self):
  out=net(self.r,'/RX5_LOAD');inp=net(self.r,'/RX5_SOURCE')
  for x in list(out):inp.append(copy.deepcopy(x))
  self.r.find('nets').remove(out);self.checkbad()
 def test_limit_resistor_removed(self):
  n=net(self.r,'/LIMIT');n.remove(n.find('node[@ref="R1"]'));self.checkbad()
 def test_limit_shorted_to_vs(self):
  n=net(self.r,'/LIMIT');n.set('name','/RX5_SOURCE');self.checkbad()
 def test_alert_shorted_to_supply(self):
  a=net(self.r,'/ALERT_N_MONITOR_ONLY');b=net(self.r,'/RX5_SOURCE')
  for x in list(a):b.append(copy.deepcopy(x))
  self.r.find('nets').remove(a);self.checkbad()
 def test_reset_disconnected(self):
  n=net(self.r,'/RX5_SOURCE');n.remove(n.find('node[@ref="U1"][@pin="5"]'));self.checkbad()
 def test_unauthorized_current_monitor_or_cut(self):
  c=ET.SubElement(self.r.find('components'),'comp',ref='U2')
  ET.SubElement(c,'value').text='SOMETHING';self.checkbad()
 def test_additional_unreviewed_net(self):
  ET.SubElement(self.r.find('nets'),'net',name='/BYPASS');self.checkbad()
 def test_unconnected_output_tied_to_alert(self):
  nc=net(self.r,'unconnected-(U1-OUT-Pad2)');self.r.find('nets').remove(nc)
  ET.SubElement(net(self.r,'/ALERT_N_MONITOR_ONLY'),'node',ref='U1',pin='2');self.checkbad()
 def test_duplicate_pin(self):
  ET.SubElement(net(self.r,'/GND'),'node',ref='U1',pin='1');self.checkbad()
 def test_duplicate_net(self):
  self.r.find('nets').append(copy.deepcopy(net(self.r,'/LIMIT')));self.checkbad()
 def test_ina_wrong_variant_rejected(self):
  self.r.find('components').find('comp[@ref="U1"]/value').text='INA301A3IDGKR';self.checkbad()
 def test_malformed_xml(self):self.assertFalse(audit(b'<export')["passed"])
 def test_missing_sections(self):self.assertFalse(audit(b'<export/>')["passed"])
 def test_wrong_root(self):self.assertFalse(audit(b'<json/>')["passed"])
 def test_missing_xml_cli(self):
  with tempfile.TemporaryDirectory() as d:
   x=Path(d);self.assertEqual(main([str(x/'missing.xml'),'--output',str(x/'report.json')]),1)
   self.assertIn('false',(x/'report.json').read_text())
 def test_positive_synthetic_cli_no_power_permission(self):
  with tempfile.TemporaryDirectory() as d:
   x=Path(d);(x/'test.xml').write_bytes(encoded(self.r))
   self.assertEqual(main([str(x/'test.xml'),'--output',str(x/'report.json')]),0)
   self.assertIn('"physical_power_authorized": false',(x/'report.json').read_text())
if __name__=='__main__':unittest.main()
