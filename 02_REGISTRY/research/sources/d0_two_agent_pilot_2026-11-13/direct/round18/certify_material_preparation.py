#!/usr/bin/env python3
"""Materialize concrete native powers; certify with outward integer intervals."""
from pathlib import Path
import hashlib,importlib.util,json,sys
import mpmath as mp
import material_targets as t
import material_preparation as compiler
P=Path(__file__).resolve().parent;D=P.parent;ROOT=P.parents[5]
OWNER=ROOT/'02_REGISTRY/research/sources/d0_native_readiness_amplification_2026-10-24/native_phase.py'
sp=importlib.util.spec_from_file_location('a18_phase',OWNER);phase=importlib.util.module_from_spec(sp);sys.modules[sp.name]=phase;sp.loader.exec_module(phase)
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()

def candidate_grid(bits):
    p=(mp.sqrt(5)-1)/2;gamma=(2**13)*mp.acos(mp.sqrt(p))/(2*mp.pi)
    x=gamma;p0,p1=0,1;q0,q1=1,0;steps=0
    while True:
        a=int(mp.floor(x));pn=a*p1+p0;qn=a*q1+q0;steps+=1
        if qn.bit_length()>=bits+20:
            return pn,qn,steps
        p0,p1=p1,pn;q0,q1=q1,qn;x=1/(x-a)

def main(bits=4096):
    precision=4*bits+256;iv=t.Dyadic(precision);constants=t.constants(iv)
    vectors={};unique={};angles={};scale=iv.scale
    with mp.workprec(3*bits+256):
        pn,qn,steps=candidate_grid(bits);inv=pow(pn,-1,qn)
        for spec in t.family_specs():
            v,psi=t.half_vector(iv,constants,spec);ro=[]
            for rotation in t.rotations(iv,v):
                geometry=compiler.plane_geometry(rotation['other'])
                cc=rotation['cos'];ss=rotation['sin']
                if ss==(0,0):
                    assert cc[0]<=scale<=cc[1]
                    ro.append({'other':rotation['other'],'angle_id':None,'exact_identity_reason':'zero target sine and positive cosine'})
                    continue
                if geometry['orientation']==-1:ss=iv.neg(ss)
                key=(*cc,*ss)
                if key not in unique:
                    aid='angle_'+str(len(unique));unique[key]=aid
                    # Candidate proposal uses mpmath; only the later exact
                    # enclosures establish the physical error assertion.
                    cm=mp.mpf(cc[0]+cc[1])/(2*scale);sm=mp.mpf(ss[0]+ss[1])/(2*scale)
                    fraction=(mp.atan2(sm,cm)/(2*mp.pi))%1
                    target_grid=int(mp.nint(qn*fraction))%qn;k=(target_grid*inv)%qn
                    assert k>0
                    _,nc,ns=phase._rotation_intervals((2**13)*k,precision)
                    err=max(abs(nc[0]-cc[1]),abs(nc[1]-cc[0]))+max(abs(ns[0]-ss[1]),abs(ns[1]-ss[0]))
                    assert err <= 2**(precision-bits),(aid,'uncertified candidate')
                    angles[aid]={'k':str(k),'k_binary_length':k.bit_length(),'native_exponent_multiplier':8192,
                        'target_cos_hex':[hex(x) for x in cc],'target_sin_hex':[hex(x) for x in ss],
                        'native_cos_hex':[hex(x) for x in nc],'native_sin_hex':[hex(x) for x in ns],
                        'denominator_power_of_two':precision,'operator_error_L1_numerator_hex':hex(err),
                        'certified_error_bits':bits}
                    if len(angles)%8==0:print('certified native material angles',len(angles),flush=True)
                ro.append({'other':rotation['other'],'angle_id':unique[key]})
            vectors[spec['id']]={'spec':spec,'half_vector_bounds_hex':{str(q):[hex(x) for x in value] for q,value in v.items()},
                                  'matter_bounds_hex':[[hex(x) for x in z] for z in psi],'rotations':ro}
    inputs=[P/'material_targets.py',P/'material_preparation.py',OWNER,D/'round14/native_boolean.py',
            t.B/'round25/TARGETS_RU.md',t.B/'round25/precision_name.py',t.B/'round21/REFERENCE_METADATA.json',
            t.B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',t.B/'round21/ORIGINAL_PF_N20_L4.jsonl']
    result={'status':'CERTIFIED_NATIVE_CAR_HALF_VECTOR_FAMILIES','schema':'d0.native.material-half-vector.v1',
        'input_sha256':{str(f):h(f) for f in inputs},'source_sha256':h(Path(__file__)),
        'precision_bits':precision,'certified_each_planar_rotation_error_le':'2^-'+str(bits),
        'uniform_q_y_preparation_error_le':'3*2^-'+str(bits),
        'max_predicate_bits':13,'private_quantum_work_count':0,
        'candidate_grid_not_certificate':{'steps':steps,'numerator':str(pn),'denominator':str(qn)},
        'vectors':vectors,'angles':angles,'catalogue':t.catalogue(),'layout':compiler.layout(),
        'norm_argument':'Exact mutually exclusive SAM/site control sectors; off-sector native parity rotations are exact identity; max active sum of at most three certified all-column plane errors, not average error.',
        'RAW_births_vacuum_Fourier_prefix_emitted':False,'full_H1_writer_emitted':False,'physical_C_closed':False,'GR_closed':False}
    (P/'MATERIAL_PREPARATION_LIBRARY.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    inv=compiler.inventory(result)
    (P/'MATERIAL_PREPARATION_INVENTORY.json').write_text(json.dumps({'library_sha256':h(P/'MATERIAL_PREPARATION_LIBRARY.json'),'banks':inv,'counts_include_all_inactive_sectors':True,'full_expanded_word_executed':False},indent=2)+'\n')
    print(json.dumps({'status':result['status'],'vectors':len(vectors),'certified_angles':len(angles),'sectors':{n:len(x) for n,x in result['catalogue'].items()},'nonidentity_rotations':{n:x['nonidentity_planar_rotation_occurrences'] for n,x in inv.items()}}))

if __name__=='__main__':main(int(sys.argv[1]) if len(sys.argv)>1 else 4096)
