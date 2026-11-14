#!/usr/bin/env python3
"""Interval-complete allocation, actual resource bindings and report semantics."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util,json,math,random,sys
import report_assembly as a
P=Path(__file__).resolve().parent;D=P.parent
plan=json.loads((P/'GLOBAL_REPORT_PLAN.json').read_text());comp=json.loads((P/'GLOBAL_REPORT_COMPILATION.json').read_text())
assert a.h(P/'report_assembly.py')==comp['source_sha256'] and a.h(P/'GLOBAL_REPORT_PLAN.json')==comp['plan_sha256']
for f,value in comp['input_sha256'].items():assert a.h(Path(f))==value,f
rng=random.Random(1735)

# The intervals prove all 1.48 billion roles are disjoint and covered without
# pretending to allocate a Hilbert vector or enumerate those RAW births.
roles=[]
for row in plan['fair_output_ranges']:roles.append((row['output_wire_start'],row['count'],'fair'))
roles += [(x,n,'golden') for x,n in plan['Golden_RAW_ranges']]
roles += [(r['range'][0],r['range'][1],r['kind']) for r in plan['source_buffers']]
roles += [(x,n,'zero') for x,n in plan['processor_zero_ranges']]
at=9;counts=Counter()
for start,width,kind in sorted(roles):
    assert width>0 and start==at,(start,width,kind,at)
    at+=width;counts[kind]+=width
assert at==plan['compiler_region_end']==plan['fair_bank_extra_start']
assert counts['zero']==plan['RAW_birth_requirements']['processor_zero']
assert counts['fair']==10248262 and counts['golden']==76
assert counts['Choi']==180*22 and counts['CAR_DATA']==16*12 and counts['CAR_RIGHT']==16*7
assert plan['logical_wire_count']==at+142*plan['fair_bank_count']
assert sum(plan['RAW_birth_requirements'].values())+9+4264==plan['logical_wire_count']
assert plan['native_wire_count_including_oldRIGHT_witness']==plan['logical_wire_count']+5

# Only eight physical SITE wires are shared; sigma has its own incoming wire.
cursor=9
for walk in plan['walks']:
    assert walk['private_start']==cursor and walk['private_width']==walk['local_wires']-8
    assert [a.global_wire(walk,i) for i in range(8)]==list(range(8))
    assert a.global_wire(walk,8)==cursor and a.global_wire(walk,walk['local_wires']-1)==cursor+walk['private_width']-1
    cursor+=walk['private_width']
assert len(set(plan['sign_wires_S1_S2_T1_to_T8']))==10
post=json.loads((D/plan['postprocessor_file']).read_text());m=plan['postprocessor_map']
assert len(m)==len(set(m))==post['wire_count']
assert [m[i] for i in post['layout']['palette']]==plan['sign_wires_S1_S2_T1_to_T8']+[8]
assert [m[i] for i in post['layout']['output']]==[plan['post_label_wire'],plan['post_READY_wire']]

# Fair output j is unique. Each 142-wire private interval is disjoint from
# all processor registers; readiness is exactly local wire85 of that bank.
prefix=0;bank_binding_checks=0
for row in plan['fair_output_ranges']:
    assert row['bank_index_start']==prefix
    for offset in sorted({0,row['count']//2,row['count']-1}):
        j=prefix+offset;output=a.fair_output(plan,j)
        assert output==row['output_wire_start']+offset
        wires=[a.fair_bank_wire(plan,j,q,output) for q in range(143)]
        assert len(set(wires))==143 and wires[84]==output
        extras=sorted(w for i,w in enumerate(wires) if i!=84)
        first=plan['fair_bank_extra_start']+142*j
        assert extras==list(range(first,first+142))
        assert a.ready_flag(plan,j)==first+84
        bank_binding_checks+=1
    prefix+=row['count']
assert prefix==plan['fair_bank_count']
ready=plan['selector_and_post_READY_wires']
assert len(ready)==len(set(ready))==1065 and ready[-1]==plan['post_READY_wire']
assert all(9<=q<plan['compiler_region_end'] for q in ready)
assert plan['READY_total_flags']==plan['fair_bank_count']+len(ready)
andstart,andwidth=plan['READY_AND_work_range'];K=plan['READY_total_flags']
assert andwidth==K-2
assert a.and_compute_gate(plan,0)[1:3]==(a.ready_flag(plan,0),a.ready_flag(plan,1))
assert a.and_core_gate(plan)==('CCX',andstart+K-3,a.ready_flag(plan,K-1),plan['all_READY_wire'])

# Exhaustive Boolean AND for arbitrary output, clean work. READY flags kept.
and_cases=0
for k in range(3,13):
    q={'fair_bank_count':0,'READY_total_flags':k,'selector_and_post_READY_wires':list(range(k)),
       'READY_AND_work_range':[k,k-2],'all_READY_wire':2*k-2}
    word=list(a.ready_logical_word(q))
    assert len(word)==2*k-3 and all(g[0]=='CCX' and g[-1]>=k for g in word)
    for flags,out in product(range(1<<k),(0,1)):
        initial=flags|(out<<(2*k-2))
        expected=initial^(int(flags==(1<<k)-1)<<(2*k-2))
        assert a.s.logic.apply_word(word,initial)==expected
        and_cases+=1

# Exact native branch proof is structural (positive controls, literal adjoint).
# Here execute actual SMALL native leaves as an independent float diagnostic:
# one failed flag must leave output/work/aux/port/Spin exactly unchanged.
q={'fair_bank_count':0,'READY_total_flags':3,'selector_and_post_READY_wires':[0,1,2],
   'READY_AND_work_range':[3,1],'all_READY_wire':4,'native_port':5,'native_spin':[6,7],'native_aux_arbitrary':8}
native=[]
for tree in a.ready_native_blocks(q,1):native.extend(a.s.nb.expand(tree,20000))
p=(math.sqrt(5)-1)/2;c=math.sqrt(p)
def numeric(word,state):
    v={state:1.0}
    for g in word:
        op=g['op'];w=g['wires'];out={}
        for x,z in v.items():
            if op=='G':
                bit=(x>>w[0])&1;base=x&~(1<<w[0])
                for y,coef in [(base,c if not bit else -p),(base|(1<<w[0]),p if not bit else c)]:out[y]=out.get(y,0)+z*coef
            elif op=='CX':
                y=x^(((x>>w[0])&1)<<w[1]);out[y]=out.get(y,0)+z
            else:
                assert op=='SourceI'
                active=(x>>w[0])&1;spin_parity=((x>>w[1])^(x>>w[2]))&1
                # Owned L_i=diag(J,-J): both Spin bits determine the sign.
                y=x^(active<<w[2]);out[y]=out.get(y,0)+z*((-1)**(active*spin_parity))
        v={x:z for x,z in out.items() if abs(z)>1e-16}
    return v
native_failure_cases=0;native_max_error=0.0
for flags,ext in product(range(7),range(16)):
    initial=flags|(ext<<5);v=numeric(native,initial)
    err=math.sqrt(sum((z-(1 if x==initial else 0))**2 for x,z in v.items())+(0 if initial in v else 1))
    assert err<1e-12,err;native_max_error=max(native_max_error,err);native_failure_cases+=1

# Actual B31 mapped native banks at first, interior and last resources.
bank=json.loads((a.B31/'NATIVE_FAIR_BANK.json').read_text());native_bindings=0;leaves=0
for j in [0,plan['fair_bank_count']//2,plan['fair_bank_count']-1]:
    tree=a.fair_bank_native(plan,j,bank)
    a.s.nb.validate_schema(tree,plan['native_wire_count_including_oldRIGHT_witness'],plan['native_port'],tuple(plan['native_spin']),(plan['protected_oldRIGHT_witness'],))
    for leaf in a.s.nb.leaves(tree):
        assert not set(leaf['wires'])&set(range(9));leaves+=1
    native_bindings+=1

# All sigma/mask addresses and exact scalar postprocessor law, conditional on
# product source copies. This deliberately does not infer that preparation.
sp=importlib.util.spec_from_file_location('a17_mass',D/'round12/compile_source_selectors.py')
owner=importlib.util.module_from_spec(sp);sys.modules[sp.name]=owner;sp.loader.exec_module(owner)
Q=owner.K;one=Q(1);p=Q(0,1)
palette=json.loads((D/'round12/TEN_SIGN_REPORT_PALETTE.json').read_text())
for j,(sigma,mask) in enumerate(palette['palette_keys']):assert j==mask+1024*int(sigma==1)
def direct_beta(f,t,sigma):
    E=p**2*(one+f/64);u=p+sigma*(p**2)*t/64
    ell=4*E*(one-E);B=4*u**2*(one-u**2);A=ell+(one-ell)*B;z=Q(F(1,2**20))
    return one-(one-z*B)*(one-z*A)
scalar_cases=0
for sigma in (-1,1):
    for ff,tt in [(F(0),F(0)),(F(1,3),F(-2,5)),(F(-1),F(1))]:
        actual=Q()
        for mask in range(1024):
            prob=F(1)
            for i in range(10):prob*=((1+(1 if mask>>i&1 else -1)*(ff if i<2 else tt))/2)
            beta=Q(*palette['partitions'][mask+1024*int(sigma==1)]['weights'][0]);actual+=beta*prob
        assert actual==direct_beta(Q(ff),Q(tt),sigma),(ff,tt,sigma)
        scalar_cases+=1
independent=sum((Q(*part['weights'][0])/1024 for part in palette['partitions'][:1024]),Q())
correlated=sum((Q(*palette['partitions'][mask]['weights'][0])/512 for mask in range(1024) if (mask&3) in (0,3)),Q())
poly=owner.report_polynomial(-1)
assert correlated-independent==poly[2,0] and correlated!=independent
for label,ready_bit,old in product((0,1),repeat=3):
    # CX(ready,r); CCX(ready,label,r) copies label0 readiness into fresh report.
    initial=label|(ready_bit<<1)|(old<<2)
    assert a.s.logic.apply_word([('CX',1,2),('CCX',1,0,2)],initial)==initial^((ready_bit*(1-label))<<2)

out={'status':'PASS_GLOBAL_REPORT_ROLE_ALLOCATION_AND_COMPONENT_COMPOSITION',
 'input_sha256':{n:a.h(P/n) for n in ['report_assembly.py','GLOBAL_REPORT_PLAN.json','GLOBAL_REPORT_COMPILATION.json']},
 'intervals_in_complete_processor_partition':len(roles),'fair_bank_boundary_and_interior_mappings':bank_binding_checks,
 'all_incoming_source_qubits':4264,'all_fresh_RAW_requirements':sum(plan['RAW_birth_requirements'].values()),
 'Boolean_READY_cases':and_cases,'small_actual_native_failed_READY_columns':native_failure_cases,
 'small_native_max_error_diagnostic':native_max_error,'actual_mapped_native_fair_banks':native_bindings,'syntactic_native_leaves_checked':leaves,
 'exact_sigma_palette_indices':2048,'exact_product_scalar_Beta_cases':scalar_cases,
 'correlated_copy_counterexample':'same marginals, nonzero difference equal to original S^2 coefficient',
 'all_report_native_calls_executed':False,'source_preparations_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'GLOBAL_REPORT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','Boolean_READY_cases','small_actual_native_failed_READY_columns','exact_product_scalar_Beta_cases','all_fresh_RAW_requirements']}))
