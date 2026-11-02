"""W-IND-32: independent native KiCad XML gate, electrical CONNECTIVITY only.

Reject any net not in the reviewed RX topology, any missing/duplicate pin,
any surprise direct VIN/EN tie, bypass or swapped stage. No safety approval.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from generate_w32 import SPECS, INSTANCES, NETS, NC

EXPECTED_PARTS={ref:val for ref,typ,x,y,val in INSTANCES}
EXPECTED={name:set(f'{r}.{p}' for r,p in pins) for name,pins in NETS.items()}
EXPECTED_NC={f'{r}.{p}' for r,p in NC}


def audit(xml:bytes):
    actual={};parts={};nc={};faults=[];seen=set()
    try:
        root=ET.fromstring(xml)
        if root.tag!='export':raise ValueError('not native KiCad <export>')
        comp=root.find('components');nets=root.find('nets')
        if comp is None or nets is None:raise ValueError('missing components/nets')
        for item in comp.findall('comp'):
            ref=item.get('ref'); val=item.findtext('value')
            if not ref or val is None or ref in parts:raise ValueError('duplicate/incomplete comp')
            parts[ref]=val
        for net in nets.findall('net'):
            name=net.get('name')
            if not name or name in actual:raise ValueError('duplicate/blank net')
            pins=set()
            for node in net.findall('node'):
                ref,num=node.get('ref'),node.get('pin')
                if not ref or not num:raise ValueError('incomplete pin')
                k=f'{ref}.{num}'
                if k in seen:raise ValueError('multiply connected pin '+k)
                seen.add(k);pins.add(k)
            if name.startswith('unconnected-'):
                if len(pins)!=1:raise ValueError('unconnected- net has >1 pins')
                nc[name]=pins
            else:
                actual[name]=pins
        if parts!=EXPECTED_PARTS:faults.append('component list, values or variants differ')
        labelled={k[1:] if k.startswith('/') else k:v for k,v in actual.items()}
        if set(labelled)!=set(EXPECTED):faults.append('unexpected/missing labels '+str(sorted(set(labelled)^set(EXPECTED))))
        for name,pins in EXPECTED.items():
            if labelled.get(name)!=pins:faults.append('mismatch '+name+' expected '+str(sorted(pins))+' got '+str(sorted(labelled.get(name,set()))))
        flat_nc=set().union(*nc.values()) if nc else set()
        if flat_nc!=EXPECTED_NC:faults.append('NC pin mismatch '+str(sorted(flat_nc^EXPECTED_NC)))
        expected_all=set().union(*EXPECTED.values())|EXPECTED_NC
        if seen!=expected_all:faults.append('pins missing/extra '+str(sorted(seen^expected_all)))
    except (ET.ParseError,ValueError,TypeError) as e:
        faults.append('invalid native XML '+str(e))
    return {'schema':'VALDO-W32-NATIVE-TOPOLOGY-V1',
            'passed':not faults, 'faults':faults,
            'status':'TOPOLOGY_MATCHES_INCOMPLETE_RX_CUT' if not faults else 'BLOCKED_TOPOLOGY',
            'net_names':sorted(actual),'parts':dict(sorted(parts.items())),
            'unconnected_pins':sorted(set().union(*nc.values()) if nc else set()),
            'two_real_rcb_devices_in_netlist':not faults,
            'actual_en_driver_built':False, 'autonomous_current_trip_built':False,
            'thermal_fod_tx_qualified':False,'emi_or_offset_measured':False,
            'lithium_connected':False,'hardware_power_authorized':False}


def main(argv=None):
    parser=argparse.ArgumentParser();parser.add_argument('native_xml',type=Path)
    parser.add_argument('--out',required=True,type=Path);args=parser.parse_args(argv)
    try:
        data=args.native_xml.read_bytes(); report=audit(data)
        report['native_xml_sha256']=sha256(data).hexdigest()
    except OSError as e:
        report=audit(b'');report['faults'].append('file IO: '+str(e));report['passed']=False
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(report['status'], '; '.join(report['faults']))
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
