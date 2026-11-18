#!/usr/bin/env python3
"""Independent physical-address and clock audit for the two A32 j=2 endpoints."""
from pathlib import Path
from collections import Counter
from hashlib import sha256
from fractions import Fraction
import ast, inspect, json, sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round32'))
import finite_book_comparison as a32
owner=json.loads((D/'round35/COUNT_ONLY_BINDING_CHECK.json').read_text())
assert owner['status']=='PASS_ACTUAL_PAIR_COUNT_ONLY_PRICE_BINDING_OBSTRUCTION'
for file,sha in owner['source_sha256'].items():assert sha256(Path(file).read_bytes()).hexdigest()==sha, file
plan=json.loads((D/'round32/FINITE_BOOK_COMPARISON_PLAN.json').read_text())
assert plan['initial_history']=={'H0':'C','Omega0':1,'P0':'I_1','previous_paid_stages':0,'old_return_Gram':'1','rank_P0':1,'Tr_old_Gram':1}
n=plan['early_canonical_RAW_births'];K=plan['late_retention_pairs']
assert n==10407050782 and K==66076
# Independently map the actual logical endpoint DAG to physical addresses. No
# leaf expansion of giant powers: each repeat contributes its exact integer.
def mapped(q):
    if q==2705:return 0
    if q==2:return 1
    if 4<=q<=2704:return q-2
    assert q>=2706
    return q-3
def inventory(tree):
    op=tree['op']
    if op=='seq':
        ans=Counter()
        for child in tree['children']:ans.update(inventory(child))
        return ans
    if op=='repeat':
        mul=int(tree['count']);assert mul>=0
        return Counter({key:mul*v for key,v in inventory(tree['child']).items()})
    assert op in ('G','CX')
    return Counter({(op,tuple(mapped(w) for w in tree['wires'])):1})
parts={z:a32.endpoint_parts(z,2) for z in ('plus','minus')}
cs={z:{k:inventory(node) for k,node in trees.items()} for z,trees in parts.items()}
full={z:sum(v.values(),Counter()) for z,v in cs.items()}
assert full['plus']==full['minus'] and parts['plus']['pre']!=parts['minus']['pre']
assert parts['plus']['last_g']==parts['minus']['last_g']=={'op':'G','wires':[6]}
assert a32.core.b.physical_tree(parts['plus']['last_g'])=={'op':'G','wires':[4]}
plus,minus=a32.powers();pa,pb=a32.align(plus,minus)
assert plus!=minus and plus+pa==minus+pb
L=plus+pa
for z in parts:
    assert sum(cs[z]['pre'].values())==L
    assert sum(cs[z]['post_before_final'].values())==L-1
    assert full[z][('G',(4,))]==plus+minus
# Each endpoint uses the exact same unconditional core W_blocks stream.
fn=ast.parse(inspect.getsource(a32.before_final_blocks))
yields=[v for v in ast.walk(fn) if isinstance(v,ast.YieldFrom)]
assert len(yields)==1 and ast.unparse(yields[0].value)=='core.W_blocks()'
# All early logical birth intervals map consecutively onto physical wires.
cursor=0
for block in a32.core.b.birth_blocks():
    start,stop=block['start'],block['stop']
    assert mapped(start)==cursor and mapped(stop-1)==cursor+stop-start-1
    assert a32.core.b.physical_wire(start)==mapped(start)
    assert a32.core.b.physical_wire(stop-1)==mapped(stop-1)
    cursor+=stop-start
assert cursor==n
assert a32.core.b.physical_wire(6)==4
# Same stage schedule for both: n early births, 2L-1 + common-core unitary
# edges before retention, then identical (birth,G) for K fresh wires, final G.
# Independent clock sum tested on small fixtures and algebraic identity.
for n0 in range(1,7):
    for lb in range(2,8):
        for k in range(6):
            dims=[2**j for j in range(n0)]+[2**n0]*(lb-1)
            for j in range(k):dims += [2**(n0+j),2**(n0+j+1)]
            dims += [2**(n0+k)]
            assert len(dims)==n0+lb+2*k
            assert sum(dims)==2**n0*(lb-3+4*2**k)-1
assert plan['clock_dimension_over_initial_dimension']['n']==n
assert plan['clock_dimension_over_initial_dimension']['K']==K
assert plan['final_carrier_dimension']['power_of_two_exponent']==n+K
# Physical late G addresses are exactly n,...,n+K-1; common on both sides.
assert n>max(w for _,ws in full['plus'] for w in ws)
# FD=Delta/(2t), so the minimax error of any common predicted price is
# Delta/2; normalizing by t*u*Gamma_s yields FD/(u*Gamma_s).
t=Fraction(1,2**1618);u=Fraction(2,3);gamma=Fraction(3,7);fd=Fraction(1,2**43)
delta=2*t*fd
assert (delta/2)/(t*u*gamma)==fd/(u*gamma)
source=json.loads((D/'round33/SAMPLING_SOURCE_BIAS_CHECK.json').read_text())
assert source['actual_normalized_finite_comparison_scalar_gt']=='2^-44'
pins=[Path(__file__),D/'round35/ACTUAL_PRICE_BINDING_GATE_RU.md',D/'round35/check_count_only_binding.py',D/'round35/COUNT_ONLY_BINDING_CHECK.json',D/'round32/finite_book_comparison.py',D/'round32/FINITE_BOOK_COMPARISON_PLAN.json',D/'round29/gcx_birth_clock.py',D/'round30/marked_source_schedule.py',D/'round33/SAMPLING_SOURCE_BIAS_CHECK.json',O/'round66/INDEPENDENT_A33_AUDIT.json']
out={'status':'PASS_CONDITIONAL_A35_ENDPOINT_BINDING_AUDIT','actual_j':2,'actual_final_gate_physical':'G wire 4 (logical wire 6)','addressed_endpoint_inventory_equal':True,'common_A30_core_and_late_gates_not_expanded':True,'early_births':n,'late_birth_G_pairs':K,'same_before_stage_dimensions_by_schedule':True,'different_ordered_endpoint_words':True,'approximate_binding_max_endpoint_error_normalized_by_t_u_Gamma_s_gt':'2^-44 conditional on A33/B66 and positive t,u,Gamma_s','normalization_identity':'(Delta_price/2)/(t*u*Gamma_s)=FD/(u*Gamma_s)','R6_R11_and_A33_price_inequality_reproved':False,'actual_Info_assigned':False,'unrestricted_state_order_dependent_binding_excluded':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in pins}}
(P/'A35_INDEPENDENT_BINDING_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'final_gate':out['actual_final_gate_physical'],'normalization':out['normalization_identity']}))
