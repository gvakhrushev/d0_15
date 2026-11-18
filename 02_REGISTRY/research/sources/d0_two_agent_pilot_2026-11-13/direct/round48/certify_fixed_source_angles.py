#!/usr/bin/env python3
"""Retune the three fixed SOURCE angle families to the two-bit budget.

The Choi prefix and Boolean/adapter phases already have 4096-bit proofs.
No old certificate or source file is changed.
"""
from pathlib import Path
from hashlib import sha256
import json,sys
sys.dont_write_bytecode=True
import two_bit_source_targets as t
from source_angle_certifier import Certifier,save_gzip
P=Path(__file__).resolve().parent
st=t.load('a48_site_targets',t.loc.B/'round45/site_targets.py')

def main():
    pins=[Path(__file__),P/'source_angle_certifier.py',P/'two_bit_source_targets.py',
          t.loc.B/'round45/site_targets.py',st.PF,t.D/'round18/material_targets.py']
    source={str(p):sha256(p.read_bytes()).hexdigest() for p in pins}
    cert=Certifier(8);iv=cert.iv;counts,specs,nodes=st.tree_names()
    angles={}
    for name,spec in specs.items():
        aid=cert.certify(*st.targets(iv,spec,counts))
        angles[name]={'spec':spec,**cert.records[aid]}
    phase=cert.certify(iv.rational(-1),iv.rational(0))
    site={'status':'CERTIFIED_RETUNED_SOURCE_SITE_NATIVE_POWERS',
      **cert.metadata(),'native_multiplier_power':8,'source_sha256':source,
      'PF_total':sum(counts),'PF_anchor':counts[0],'tree_nodes':nodes,
      'angles':angles,'reflection_phase':cert.records[phase]}
    save_gzip(P/'RETUNED_SITE_LIBRARY.json.gz',site)
    fixed={}
    for name,K,target in [('fourier_pi_over_2',7,(0,1)),('joint_reflection_pi',46,(-1,0))]:
        cert=Certifier(K);iv=cert.iv
        aid=cert.certify(iv.rational(target[0]),iv.rational(target[1]))
        fixed[name]={**cert.metadata(),'selected_angle_id':aid,'k':cert.records[aid]['k']}
    out={'status':'CERTIFIED_RETUNED_FOURIER_AND_JOINT_REFLECTION',
      'source_sha256':source,'fixed_angles':fixed,'new_full_SOURCE_compiled':False,
      'physical_C_closed':False,'GR_closed':False}
    (P/'RETUNED_FIXED_ANGLES.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'site_tree_angles':len(angles),
      'site_tree_nodes':len(nodes),'per_macro_error_le':'2^-3456'}))

if __name__=='__main__':main()
