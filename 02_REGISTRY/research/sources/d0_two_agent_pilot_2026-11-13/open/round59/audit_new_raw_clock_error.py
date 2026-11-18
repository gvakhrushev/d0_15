#!/usr/bin/env python3
"""Independent A29 RAW coordinates, clock dimensions and rational error audit."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,random,sys
import sympy as s
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=Path(__file__).resolve().parent.parent;P=O/'round59';sys.path.insert(0,str(D/'round29'));import gcx_birth_clock as b
c=b.c;g=c.old;ns=g.namespace();N=ns['layout']['qubits'];plan=json.loads((D/'round29/GCX_BIRTH_CLOCK_PLAN.json').read_text());old=json.loads((D/'round25/GLOBAL_H1_PLAN.json').read_text());census=json.loads((O/'round58/CZ_EXACT_OCCURRENCES.json').read_text());cert=json.loads((O/'round57/GADGET_G_POWER_CERTIFICATE.json').read_text());rnd=random.Random(5911);n=N-2;assert n==10407050782 and plan['total_RAW_births']==n
# Independent address formulas by chronological role; all m old coordinates
# are external, including m=0; the resulting ranges are adjacent.
def expected(q,m):
 if q==2705:return m
 if q==2:return m+1
 if 4<=q<=2704:return m+q-2
 assert 2706<=q<=N;return m+q-3
cases=[]
for m in (0,1,3,17,103):
 blocks=b.birth_blocks();cursor=m
 for block in blocks:
  lo,hi=block['start'],block['stop'];assert expected(lo,m)==cursor and expected(hi-1,m)==cursor+hi-lo-1
  cursor+=hi-lo
 assert cursor==m+n
 samples=[q for q in range(2707) if q not in (0,1,3)]+[N,N-1]+[rnd.randrange(2706,N) for _ in range(300)]
 for q in samples:
  p=expected(q,m);assert b.physical_wire(q,m)==p and b.logical_wire(p,m)==q and p>=m
 for q in range(m):assert b.logical_wire(q,m) is None
 assert b.physical_wire(2692,m)==m+2690 and b.physical_wire(2705,m)==m
 cases.append({'m':m,'samples':len(samples),'new_helper':m+n-1})
# Actual final primitive of new compiled SITE-inverse block, without giant
# word expansion or a free closing gate.
q=2692;initial=nb=g.nb.rotation_power(q,-1,2705,(0,1));last_old=g.nb.inverse_literal(initial,2705,(0,1));last_new,pending,_=c.production_compiler().transform(last_old);assert not pending
def last(t):
 while t['op'] in ('seq','repeat'):t=t['children'][-1] if t['op']=='seq' else t['child']
 return t
final=last(last_new);assert final=={'op':'CX','wires':[2692,2705]}
L=int(plan['native_call_count_L']);clock=int(plan['clock_layers_N']);assert clock==L+n and L.bit_length()==11647 and clock<2**11647
for j in range(1,12):
 for ell in range(1,12):assert sum(2**i for i in range(j))+ell*2**j==(ell+1)*2**j-1
# Exact finite Book G1-G5 clock with two growing births and true final gate.
# sqrt(p)^2+p²=1 from p²+p=1; simplify exact radicals, not a float test.
p=(s.sqrt(5)-1)/2;v=s.Matrix([s.sqrt(p),p]);J0=v;J1=s.kronecker_product(s.eye(2),v);D1=s.eye(2)-J0*J0.T;D2=s.eye(4)-J1*J1.T;B0=J1*J0;B1=J1;R=B0.T.col_join(D1*B1.T).col_join(D2).col_join(s.zeros(4))
U=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]);G=s.Matrix([[s.sqrt(p),-p],[p,s.sqrt(p)]]);last_gate=s.kronecker_product(s.eye(2),G);assert any(s.simplify(x)!=0 for x in U*last_gate-last_gate*U);dims=[1,2,4,4];idx=[0,1,3,7,11];T=s.zeros(11)
for j,Fj in enumerate((J0,J1,U)):T[idx[j+1]:idx[j+2],idx[j]:idx[j+1]]=Fj
T[:,7:11]=R*last_gate
assert all(s.simplify(x)==0 for x in R.T*R-s.eye(4))
assert all(s.simplify(x)==0 for x in T.T*T-s.eye(11)) and all(s.simplify(x)==0 for x in T*T.T-s.eye(11))
# Exact old+new error, and independently stated normalized bounds.
e=old['compressed_reflection_error_bound'];old_bound=F(int(e['numerator_hex'],16),int(e['denominator_hex'],16));pairs=int(census['W_nonCZ_SourceI_pair_count']);C=census['W_CZ_total'];rot=2*pairs+4*C;assert rot<2**4188
replace=F(rot,2**7432);total=old_bound+replace
assert replace<F(1,2**3244) and total<F(1,2**3231)
assert F(67,100)-total>F(2,3)
assert total*2**3158 < F(1,2**73)
assert 55*total*2**3158 < F(1,2**67)
assert 55*total*2**3188 < F(1,2**37)
r=plan['all_column_replacement_error_bound'];assert F(int(r['numerator_hex'],16),int(r['denominator_hex'],16))==replace
r=plan['canonical_compressed_error_bound'];assert F(int(r['numerator_hex'],16),int(r['denominator_hex'],16))==total
# ST4 witness: extend both old witnesses by the same freshly born helper;
# single matrix element changes by at most all-column norm error.
base=F(24,25)*F(309,500)**7;assert base-replace>F(3,100)
paths=[D/'round29/gcx_compiler.py',D/'round29/gcx_birth_clock.py',D/'round29/GCX_BIRTH_CLOCK_PLAN.json',D/'round25/GLOBAL_H1_PLAN.json',O/'round58/CZ_EXACT_OCCURRENCES.json',O/'round57/GADGET_G_POWER_CERTIFICATE.json']
out={'status':'PASS_INDEPENDENT_A29_RAW_CLOCK_ERROR','m_cases':cases,'births':n,'native_gate_count_bit_length':L.bit_length(),'isolated_N_lt':'2^11647','clock_dimension_formula':'D/d0=(L+1)*2^n-1','exact_two_birth_clock_unitary':True,'actual_last_native_gate':final,'new_replacement_error_lt':'2^-3244','old_plus_new_compressed_error_lt':'2^-3231','exact_sum_times_2^3231_numerator_hex':hex((total*2**3231).numerator),'exact_sum_times_2^3231_denominator_hex':hex((total*2**3231).denominator),'scalar_c_gt':'2/3 conditional B58 and ideal source law','native_error_bounds':['2^-73','2^-67','2^-37'],'ST4_commutator_gt':'3/100 for front-loaded births','actual_heat_derivative_or_complete_physical_C_proved':False,'source_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in paths},'GR_closed':False}
(P/'A29_RAW_CLOCK_ERROR_INDEPENDENT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'births':n,'m_cases':len(cases),'old_plus_new_ratio':float(total*2**3231),'exact_clock':True}),flush=True)
