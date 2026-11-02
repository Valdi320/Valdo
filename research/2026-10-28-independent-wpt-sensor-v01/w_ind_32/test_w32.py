"""W-IND-32 deterministic KiCad generator / XML mutation tests, no hardware."""
from __future__ import annotations
import copy
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import generate_w32 as g
from netlist_gate_w32 import audit, EXPECTED, EXPECTED_NC, EXPECTED_PARTS, main


def fixture():
    root=ET.Element('export');parts=ET.SubElement(root,'components');nets=ET.SubElement(root,'nets')
    for ref,val in EXPECTED_PARTS.items():
        c=ET.SubElement(parts,'comp',ref=ref);ET.SubElement(c,'value').text=val
    for i,(name,pins) in enumerate(EXPECTED.items()):
        net=ET.SubElement(nets,'net',name='/'+name,code=str(i+1))
        for item in sorted(pins):
            ref,num=item.rsplit('.',1);ET.SubElement(net,'node',ref=ref,pin=num)
    for i,item in enumerate(sorted(EXPECTED_NC)):
        ref,num=item.rsplit('.',1)
        net=ET.SubElement(nets,'net',name=f'unconnected-({ref}-PIN-{num})',code=str(99+i))
        ET.SubElement(net,'node',ref=ref,pin=num)
    return root


def asxml(r):return ET.tostring(r,encoding='utf-8')
def find(r,name):return next(x for x in r.find('nets') if x.get('name')=='/'+name)

def move(r,src,dst,ref,pin):
    n=find(r,src);p=next(x for x in n if x.get('ref')==ref and x.get('pin')==pin)
    n.remove(p);find(r,dst).append(p)

def short(r,left,right):
    a=find(r,left);b=find(r,right)
    for p in list(b):a.append(copy.deepcopy(p))
    r.find('nets').remove(b)

class Generator(unittest.TestCase):
    def test_01_stable_identifiers(self):self.assertEqual(g.uid('U1'),g.uid('U1'))
    def test_02_all_uuids_unique(self):self.assertEqual(len({g.uid(r) for r,*_ in g.INSTANCES}),len(g.INSTANCES))
    def test_03_rpw_10pins_only(self):
        pins=g.SPECS['TPS259470_RPW10'][2]
        self.assertEqual({p[0]:p[1] for p in pins},{'1':'EN/UVLO','2':'OVLO','3':'AUXOFF','4':'FLT_N','5':'IN','6':'OUT','7':'DVDT','8':'GND','9':'ILM','10':'ITIMER'})
    def test_04_two_rcb_stages_correct_variant(self):
        self.assertEqual([v for r,t,x,y,v in g.INSTANCES if t=='TPS259470_RPW10'],['TPS259470LRPWR']*2)
    def test_05_no_duplicate_pin_or_hidden_unwired(self):
        ls=[p for n in g.NETS.values() for p in n]+g.NC
        self.assertEqual(len(ls),len(set(ls)))
        self.assertEqual(set(ls),set(g.coordinates()))
    def test_06_two_serial_stage_nets(self):
        self.assertEqual(g.NETS['RX5_BETWEEN_CUTS'],[('U2','6'),('U3','5')])
        self.assertEqual(g.NETS['RX5_POST_SHUNT'],[('RSH1','2'),('U2','5')])
        self.assertEqual(g.NETS['RX5_LOAD'],[('U3','6'),('J2','1')])
    def test_07_individual_pull_down(self):
        self.assertEqual(set(g.NETS['PERMIT_A_UNQUALIFIED']),{('J3','1'),('RPD1','1'),('U2','1')})
        self.assertEqual(set(g.NETS['PERMIT_B_UNQUALIFIED']),{('J4','1'),('RPD2','1'),('U3','1')})
    def test_08_alert_is_readonly(self):
        self.assertNotIn(('U2','1'),g.NETS['ALERT_N_READ_ONLY'])
        self.assertNotIn(('U3','1'),g.NETS['ALERT_N_READ_ONLY'])
    def test_09_current_sense_kelvin(self):
        self.assertEqual(set(g.NETS['KELVIN_PLUS']),{('RSH1','3'),('U1','8')})
        self.assertEqual(set(g.NETS['KELVIN_MINUS']),{('RSH1','4'),('U1','7')})
    def test_10_generator_repeatable(self):
        for name,content in g.render_files().items():
            self.assertEqual((Path(__file__).parent/name).read_text(),content)
    def test_11_false_safety_resistor_values_block(self):
        vals=[v for _,_,_,_,v in g.INSTANCES]
        self.assertIn('RILM_A_TBD',vals);self.assertIn('CIT_A_TBD',vals)
    def test_12_no_battery_or_tx_connections(self):
        self.assertFalse(any('BMS' in n or n.startswith('TX_') for n in g.NETS))

class NativeXMLMutation(unittest.TestCase):
    def setUp(self):self.r=fixture()
    def reject(self):
        obj=audit(asxml(self.r));self.assertFalse(obj['passed'],obj)
        self.assertFalse(obj['hardware_power_authorized'])
    def test_13_valid_synthetic_topology_not_power_approval(self):
        obj=audit(asxml(self.r));self.assertTrue(obj['passed'],obj['faults'])
        self.assertFalse(obj['actual_en_driver_built']);self.assertFalse(obj['hardware_power_authorized'])
    def test_14_bypass_cut_a(self):short(self.r,'RX5_POST_SHUNT','RX5_BETWEEN_CUTS');self.reject()
    def test_15_bypass_cut_b(self):short(self.r,'RX5_BETWEEN_CUTS','RX5_LOAD');self.reject()
    def test_16_bypass_entire_chain(self):short(self.r,'RX5_POST_SHUNT','RX5_LOAD');self.reject()
    def test_17_short_source_output(self):short(self.r,'RX5_SOURCE','RX5_LOAD');self.reject()
    def test_18_short_en_a_to_input(self):short(self.r,'PERMIT_A_UNQUALIFIED','RX5_SOURCE');self.reject()
    def test_19_short_en_b_to_input(self):short(self.r,'PERMIT_B_UNQUALIFIED','RX5_SOURCE');self.reject()
    def test_20_link_en_a_en_b(self):short(self.r,'PERMIT_A_UNQUALIFIED','PERMIT_B_UNQUALIFIED');self.reject()
    def test_21_alert_controls_en(self):short(self.r,'ALERT_N_READ_ONLY','PERMIT_A_UNQUALIFIED');self.reject()
    def test_22_remove_first_pulldown(self):move(self.r,'PERMIT_A_UNQUALIFIED','GND','RPD1','1');self.reject()
    def test_23_remove_second_pulldown(self):move(self.r,'PERMIT_B_UNQUALIFIED','GND','RPD2','1');self.reject()
    def test_24_swap_kelvin_inputs(self):move(self.r,'KELVIN_PLUS','KELVIN_MINUS','U1','8');self.reject()
    def test_25_short_kelvin_plus_minus(self):short(self.r,'KELVIN_PLUS','KELVIN_MINUS');self.reject()
    def test_26_change_efuse_variant(self):
        self.r.find('components').find('comp[@ref="U2"]/value').text='TPS259474LRPWR';self.reject()
    def test_27_delete_efuse(self):self.r.find('components').remove(self.r.find('components').find('comp[@ref="U2"]'));self.reject()
    def test_28_remove_ground(self):move(self.r,'GND','ILM_A','U2','8');self.reject()
    def test_29_duplicate_pin(self):ET.SubElement(find(self.r,'GND'),'node',ref='U2',pin='1');self.reject()
    def test_30_duplicate_net(self):self.r.find('nets').append(copy.deepcopy(find(self.r,'LIMIT')));self.reject()
    def test_31_add_unapproved_net(self):ET.SubElement(self.r.find('nets'),'net',name='/BYPASS');self.reject()
    def test_32_connect_nc_auxoff(self):
        n=next(x for x in self.r.find('nets') if 'U2-PIN-3' in (x.get('name') or ''))
        self.r.find('nets').remove(n)
        ET.SubElement(find(self.r,'RX5_SOURCE'),'node',ref='U2',pin='3');self.reject()
    def test_33_missing_nc(self):
        n=next(x for x in self.r.find('nets') if 'U2-PIN-7' in (x.get('name') or ''))
        self.r.find('nets').remove(n);self.reject()
    def test_34_bad_root(self):self.assertFalse(audit(b'<bad/>')['passed'])
    def test_35_truncated_xml(self):self.assertFalse(audit(b'<export>')['passed'])
    def test_36_no_components(self):self.assertFalse(audit(b'<export><nets/></export>')['passed'])
    def test_37_cli_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.assertEqual(main([str(p/'missing.xml'),'--out',str(p/'r.json')]),1)
            self.assertIn('"hardware_power_authorized": false',(p/'r.json').read_text())
    def test_38_cli_synthetic_pass_but_cannot_approve(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'x.xml').write_bytes(asxml(self.r))
            self.assertEqual(main([str(p/'x.xml'),'--out',str(p/'r.json')]),0)
            self.assertIn('"hardware_power_authorized": false',(p/'r.json').read_text())

if __name__=='__main__':unittest.main()
