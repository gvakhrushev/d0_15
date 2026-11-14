#!/usr/bin/env python3
"""Concrete certified pi powers for K8 SITE and K46 Choi joint reflection."""
from pathlib import Path
import hashlib,importlib.util,json,sys
import mpmath as mp
import gray_reflection as g
P=Path(__file__).resolve().parent;D=P.parent;sys.path.insert(0,str(D/'round20'))
import coframe_targets as t
s=importlib.util.spec_from_file_location('a22_powers',D/'round20/certify_coframe_angles.py');power=importlib.util.module_from_spec(s);sys.modules[s.name]=power;s.loader.exec_module(power)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    bits=3264;precision=7168;iv=t.Dyadic(precision);c=t.constants(iv);S=iv.scale;entries={}
    tc,ts=iv.rational(-1),iv.rational(0)
    with mp.workprec(3*bits+256):
        for K in (8,46):
            pn,qn,steps=power.candidate_grid(bits+4,K);inverse=pow(pn,-1,qn)
            grid=int(mp.nint(mp.mpf(qn)/2))%qn;k=(grid*inverse)%qn;assert k>0
            nc,ns=power.native_power((1<<K)*k,iv,c)
            err=max(abs(nc[0]-tc[1]),abs(nc[1]-tc[0]))+max(abs(ns[0]-ts[1]),abs(ns[1]-ts[0]))
            assert err<=1<<(precision-bits)
            entries[str(K)]={'controls':K,'k':str(k),'k_binary_length':k.bit_length(),
                             'native_exponent_multiplier':1<<K,'native_cos_hex':[hex(x) for x in nc],'native_sin_hex':[hex(x) for x in ns],
                             'target_cos_hex':[hex(x) for x in tc],'target_sin_hex':[hex(x) for x in ts],
                             'error_L1_numerator_hex':hex(err),'denominator_power_of_two':precision,'uniform_operator_error_le':'2^-3264',
                             'candidate_grid_not_proof':{'numerator':str(pn),'denominator':str(qn),'steps':steps},
                             'forward_counts':{q:str(v) for q,v in g.counts(K,k).items()},
                             'literal_inverse_counts':{q:str(v) for q,v in g.counts(K,k,1).items()},
                             'new_clean_wires':0,'off_anchor_exact_identity':True,'aux_may_be_arbitrary':True}
            print('certified scratch-free reflection K',K,flush=True)
    out={'status':'CERTIFIED_ACTUAL_GRAY_JOINT_REFLECTION_POWERS','precision_bits':precision,'entries':entries,
         'source_sha256':h(Path(__file__)),'input_sha256':{str(p):h(p) for p in [P/'gray_reflection.py',D/'round20/certify_coframe_angles.py',D/'round20/coframe_targets.py',D/'round18/material_targets.py',D/'round14/native_boolean.py']},
         'exact_forward_involution_claimed':False,'history_equated_to_A13_comparator':False,
         'full_huge_word_executed':False,'physical_C_closed':False,'GR_closed':False}
    (P/'GRAY_REFLECTION_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'controls':[8,46],'error_le':'2^-3264','new_clean_work':0}))
if __name__=='__main__':main()
