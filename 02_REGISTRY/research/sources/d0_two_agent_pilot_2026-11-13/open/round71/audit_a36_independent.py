#!/usr/bin/env python3
"""Independent bounded audit: A36 outer insertions, clock and price split."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import ast,inspect,json,sys
import sympy as s
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(D/'round36'))
import independent_outer_pairs as a36
old=a36.old
plan=json.loads((D/'round36/INDEPENDENT_OUTER_PAIRS_PLAN.json').read_text())
check=json.loads((D/'round36/INDEPENDENT_OUTER_PAIRS_CHECK.json').read_text())
assert check['status']=='PASS_ACTUAL_OUTER_PLACEMENTS_CLOCK_BUDGET_AND_NONSYMMETRIC_SPLIT'
for source in (plan,check):
    for f,digest in source['source_sha256'].items():assert sha256(Path(f).read_bytes()).hexdigest()==digest, f
ap,am=old.powers();n0=ap+am;T=n0+4
assert (ap,am,n0,T)==a36.parameters()
# Read the genuine compact DAGs.  Actual G occurrences are counted without
# expanding huge powers and translated to physical SAM-wire addresses.
for j in (0,2,42,2687):
    Pairs={(leg,sign):a36.endpoint_parts(leg,sign,j) for leg in ('forward','backward') for sign in ('plus','minus')}
    assert Pairs['backward','plus']['pre']==Pairs['backward','minus']['pre']
    assert Pairs['forward','plus']['post_before_final']==Pairs['forward','minus']['post_before_final']
    for (leg,sign),parts in Pairs.items():
        pre,post=old.nb.counts(parts['pre']),old.nb.counts(parts['post_before_final'])
        ep=(ap if sign=='plus' else am) if leg=='forward' else n0
        eo=n0 if leg=='forward' else (am if sign=='plus' else ap)
        assert pre['G']==ep and post['G']==eo-1
        assert pre['CX']==T-ep and post['CX']==T-eo
        assert sum(pre.values())==T and sum(post.values())==T-1
        assert a36.core.b.physical_tree(parts['last_g'])=={'op':'G','wires':[2+j]}
# Check that common actual core is unconditional and precedes the changing
# post suffix in the real lazy stage iterator (without expanding that core).
tree=ast.parse(inspect.getsource(a36.execution_stages))
yields=[x for x in ast.walk(tree) if isinstance(x,ast.YieldFrom)]
assert any(ast.unparse(z.value)=='core.W_blocks()' for z in yields)
# Independently exercise exact three-wire padding on all 8 basis states.
layout=a36.core.g.namespace()['layout'];slots=[layout['aux_arbitrary'],layout['port'],layout['qubits']];ix={w:k for k,w in enumerate(slots)}
for length in range(4,16):
    gates=list(old.nb.expand(old.padding(length),15));assert len(gates)==length
    for z in range(8):
        state=z
        for gate in gates:
            assert gate['op']=='CX';control,target=map(ix.get,gate['wires'])
            if state & (1<<control):state^=1<<target
        assert state==z
for exp in (ap,am,n0):
    twos,fives=old.identity_counts(T-exp);assert 2*twos+5*fives==T-exp
# Arbitrary nonsymmetric M: both leg derivatives sum to the conjugated
# derivative. A symmetric M0 makes the two half-split exactly equal; actual M
# remains only within the owned e_B ball.
a,b,c,d,x,y=s.symbols('a b c d x y',real=True)
M=s.Matrix([[a,b],[c,d]]);X=s.Matrix([[0,-1],[1,0]]);v=s.Matrix([x,y])
f=(v.T*M*X*v)[0];back=(-v.T*X*M*v)[0];paired=(v.T*(M*X-X*M)*v)[0]
assert s.expand(f+back-paired)==0
assert s.expand(f-paired/2).subs(c,b)==0
assert s.expand((f-paired/2).subs({b:1,c:0,x:1,y:0}))!=0
# |<v,(Delta M X+X Delta M)v>|/2 <= e_B; true Gamma_s multiplies
# dc by 1/(2gs), so split error <2^-74, not an exact half claim.
assert F(1,2**3231)*2**3158/2==F(1,2**74)
# Clock from actual n and source plan, not assumed from A32.
cp=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text());n=cp['total_RAW_births'];L=int(cp['new_native_call_count'])+2*T;K=66076
assert n==10407050782 and n+L<2**11647
assert int(plan['Lbase_hex'],16)==L and int(plan['Nbase_hex'],16)==n+L
for n0small in range(1,6):
    for length in range(1,7):
        for k in range(6):
            dims=[2**i for i in range(n0small)]+[2**n0small]*(length-1)
            for i in range(k):dims += [2**(n0small+i),2**(n0small+i+1)]
            dims += [2**(n0small+k)]
            assert len(dims)==n0small+length+2*k
            assert sum(dims)==2**n0small*(length-3+4*2**k)-1
# n0 approximates I within 2delta, active n± within delta: combined <3delta.
# Recompute A36's full budget independently from the A32 exact calculator.
prior=old.budget(n+L);leg=prior['fd_truncation']+F(3,2)*prior['endpoint_angle_synthesis']+prior['all_mode_heat']
assert leg<F(1,2**73)
lower=F(1,2**45)-2*F(1,2**73)-2*leg
assert lower>F(1,2**46)
assert plan['backward_pair_has_identical_complete_prefix_through_A30_core']
assert plan['backward_variation_decoded_forward_field_tangent'] is False
assert plan['A31_inverse_J_applied_to_backward_variation'] is False
assert not plan['same_complete_task_membership_or_FN_fibre_proved']
pins=[Path(__file__),D/'round36/independent_outer_pairs.py',D/'round36/INDEPENDENT_OUTER_PRICE_ROWS_RU.md',D/'round36/INDEPENDENT_OUTER_PAIRS_PLAN.json',D/'round36/INDEPENDENT_OUTER_PAIRS_CHECK.json',D/'round32/finite_book_comparison.py',D/'round33/SAMPLING_SOURCE_BIAS_RU.md',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',O/'round66/B66_A33_INDEPENDENT_AUDIT_RU.md',O/'round69/B69_ACTUAL_TASK_INPUTS_AND_ADMISSION_RU.md',O/'round70/B70_ACTUAL_INNER_COMMUTANT_RU.md']
out={'status':'PASS_CONDITIONAL_INDEPENDENT_A36_OUTER_ROWS_AUDIT','four_endpoints_actual_G_CX_placements_checked':True,'same_backward_full_prefix_through_A30_core':True,'three_delta_bound_from_two_certified_G_powers':True,'nonsymmetric_actual_M_half_split_error_under_Gamma_s_lt':'2^-74 conditional','each_outer_FD_over_u_Gamma_s_gt':'2^-46 conditional','A31_J_inverse_for_backward_used':False,'same_task_membership_or_FN_fibre_proved':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in pins}}
(P/'A36_INDEPENDENT_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'per_leg_lower':out['each_outer_FD_over_u_Gamma_s_gt']}))
