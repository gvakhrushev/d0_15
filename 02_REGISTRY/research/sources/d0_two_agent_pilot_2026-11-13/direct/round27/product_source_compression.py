#!/usr/bin/env python3
"""Bind existing full source copies and the actual SC6 polynomial.

Exact finite interface/arithmetic checks supplement the written product-state
and rank-two moment proof. They do not run the full native source word or
establish physical marks/birth/Cost-Info admission.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,itertools,json,sys
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round25'));import global_h1 as g
def main():
    ns=g.namespace();rows=[json.loads(s) for s in (g.B/'round25/COPY_SLOTS.jsonl').read_text().splitlines()]
    translate={'Choi':'Choi','material':'CAR'}
    actual={(s['bank'],s['walk'],s['kind'],s['copy']) for s in ns['source_slots']}
    wanted={(s['bank'],s['sign'],translate[s['type']],s['copy']) for s in rows}
    assert len(rows)==len(actual)==len(wanted)==1372 and actual==wanted
    per_walk={}
    for bank in g.ns.BANKS:
        for name in ['S1','S2',*['T'+str(i) for i in range(1,9)]]:
            slots=[s for s in ns['source_slots'] if s['bank']==bank and s['walk']==name]
            counts=Counter(s['kind'] for s in slots)
            assert counts==({'Choi':82} if name[0]=='S' else {'Choi':2,'CAR':2})
            for kind in counts:
                assert sorted(s['copy'] for s in slots if s['kind']==kind)==list(range(counts[kind]))
            per_walk[bank+'/'+name]=dict(counts)
    # B49 derives these normal forms from ALL actual SC6 primitive letters.
    normal=json.loads((g.B/'round49/SC6_ACTIVE_PORT_OWNER_CHECK.json').read_text())['term_normal_forms']
    terms=[(z['selector'],z['sign'],*z['call_indices']) for z in normal]
    assert len(terms)==8 and len({z[0] for z in terms})==8 and all(s.count('1')==2 for s,_,_,_ in terms)
    # Multilinear coefficient vector of event probability / (kappa p^7).
    polynomial=Counter()
    for selector,sign,i,j in terms:
        if sign<0:polynomial[()]+=1
        polynomial[tuple(sorted((i,j)))]+=sign
    expected=Counter({():4,(0,2):1,(1,3):1,(0,3):-1,(1,2):-1,
                      (4,6):1,(3,5):1,(3,4):-1,(5,6):-1})
    assert dict(polynomial)==dict(expected)
    # Every report's two bits are used ONLY through event READY & REPORT.
    # Enumerate 4^7 patterns; all 8 selectors have weight p^7 under RAW v.
    cases=0
    for pairs in itertools.product(range(4),repeat=7):
        events=[int(v==3) for v in pairs]
        direct=sum(events[i]*events[j] if sign>0 else 1-events[i]*events[j] for _,sign,i,j in terms)
        cross=4+(events[0]-events[1])*(events[2]-events[3])+(events[4]-events[5])*(events[6]-events[3])
        assert direct==cross;cases+=1
    # Independent symbolic coefficient check: expectation of multi-affine
    # truth under product probabilities equals substitution of P_j.
    moment=[F(1,11),F(2,13),F(3,17),F(4,19),F(5,23),F(6,29),F(7,31)]
    averaged=F()
    for bits in itertools.product((0,1),repeat=7):
        weight=F(1)
        for b,p in zip(bits,moment):weight*=p if b else 1-p
        value=4+(bits[0]-bits[1])*(bits[2]-bits[3])+(bits[4]-bits[5])*(bits[6]-bits[3])
        averaged+=weight*value
    target=4+(moment[0]-moment[1])*(moment[2]-moment[3])+(moment[4]-moment[5])*(moment[6]-moment[3])
    assert averaged==target
    # Fourier128 row mass: 64 full cos/sin pairs, coefficient 1/128.
    assert F(64,128**2)==F(1,256)
    A=2049;N=32*A
    assert N==65568 and N//2==32784
    # Anchor moment coefficients: (N/2)*2*(1/sqrt N)*(J/sqrt N)=J.
    assert F(N,2)*2/F(N)==1 and F(N)*2/F(N)==2
    # PF is sampled once after the cross product. A generic exact covariance
    # example refutes replacing that by independent averages; it is not a
    # new physical field construction.
    pf=[F(1,3),F(2,3)];dy=[F(1,4),F(3,4)];df=[F(1,5),F(4,5)]
    joint=sum((w*y*f for w,y,f in zip(pf,dy,df)),F())
    separate=sum((w*y for w,y in zip(pf,dy)),F())*sum((w*f for w,f in zip(pf,df)),F())
    assert joint-separate==F(1,15)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    pins=[Path(__file__),D/'round25/H1_NAMESPACE_PLAN.json',D/'round25/GLOBAL_H1_PLAN.json',
          D/'round26/FULL_READY_GAIN_CHECK.json',D/'round17/GLOBAL_REPORT_ASSEMBLY_RU.md',
          D/'round11/FULL_SOURCE_OPERATOR_RU.md',g.B/'round25/COPY_SLOTS.jsonl',g.B/'round25/TARGETS_RU.md',
          g.B/'round33/OPERATOR_COMPRESSION_RU.md',g.B/'round49/SC6_ACTIVE_PORT_OWNER_CHECK.json']
    out={'status':'EXACT_SOURCE_SLOT_AND_SC6_PRODUCT_COMPRESSION_CHECK',
         'source_sha256':{str(p):sha(p) for p in pins},'source_slots_bound_to_original_B25':1372,
         'explicit_type_translation':translate,'per_bank_walk_copies':per_walk,'SC6_terms_consumed_from_actual_word_audit':terms,
         'SC6_all_READY_REPORT_patterns_checked':cases,
         'click_over_kappa_p7':'4+(P_yplus-P_yminus)*(P_f-P_0)+(P_xplus-P_xminus)*(P_q-P_0)',
         'condition_for_multilinear_substitution':'conditional on SAM=b and common SITE=x, seven ideal report input/state/resources are products across private report arenas',
         'Choi_original_active_addresses':A,'Choi_original_anchor_N':N,'Fourier_row_mass':'1/256',
         'PF_covariance_counterexample':'1/15 for generic algebraic probability variables, not a physical field witness',
         'proof_of_full_original_geometric_moments_is_in_companion_document_and_consumed_owners':True,
         'full_giant_native_source_word_executed':False,'original_marked_map_or_physical_admission_proved':False,'physical_C_closed':False,'GR_closed':False}
    (P/'PRODUCT_SOURCE_COMPRESSION_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'source_slots':1372,'SC6_patterns':cases}))
if __name__=='__main__':main()
