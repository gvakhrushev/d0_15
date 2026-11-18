#!/usr/bin/env python3
"""Independently check A43 rational budget and literal two-slot recipe."""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as F
import sympy as sp
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
A=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.path.insert(0,str(A/'round43'));import local_q_price as a
s=F(1,2**30);nu=F(3,5);eb=F(1,2**3231);ew=F(1,2**3244);eu=F(1,2**14623);gs=F(1,2**3158)
assert F(2,25)+16*s<F(1,8)
assert 24/(1-24*s)<25 and F(17,16)**4<F(4,3)
linkerr=F(4,3)*25
assert linkerr<34 and 4*34*F(3,2)**3==459
fd=3*F(400,9)*2*(4*6+2*459)*s
assert fd==251200*s and fd<F(2**18)*s
qd=2/nu**2*(s/F(64)+4*s*s+2*(nu+s)*s)
assert qd<8*s
report=F(2**47,2**1531)*2**26+24*F(2**43,2**1531)*16**2
assert report<F(1,2**1457)
edge=F(1,4**4)*(fd*s+24*qd*s)+2*report
assert edge<2**11*s*s
ratio=2*edge/s+2*eb/gs
assert ratio<F(1,2**17)
lam=F(9,4)*s
qerr=F(3,8)*((lam**2/2+2*ew)*ratio+2*ew/gs)+eu/gs
assert qerr<F(1,2**77)
oldlower=s/6400-F(2**10)*s*s-F(1,2**1426)-F(1,2**73)
reduced=oldlower/2-F(1,2**2870)
assert reduced>F(1,2**44)
cfg=a.extend_configuration(a.old.production_configuration())
assert cfg['Nbase'].bit_length()==25457 and cfg['K']==137444
budget=a.budget(cfg)
assert budget['pointwise_local_f_derivative_bound']==fd
assert budget['pointwise_local_q_derivative_bound']==qd
assert budget['concrete_j2_reduced_Pf_lower']==reduced
qcap=F(3,8)*((lam**2/2+2*ew)*F(1,2**17)+2*ew/gs)+eu/gs
assert budget['Qb_analytic_minus_half_ideal_Pf_bound']==qcap and qcap>=qerr
z,t=F(1,2**20),F(1,2**1618)
bracket=8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
taylor=t*t*bracket/(16*gs)
angular=F(1,2**4852)/(t*gs)
heat=F(6*cfg['Nbase'],359)/(t*(F(8,3)*z*gs))*F(1,2**(cfg['K']//4))
finite=taylor+angular+heat
assert budget['Q_full_finite_price_vs_analytic_error']==finite
assert qcap+finite<F(1,2**75)
assert reduced/2-qcap-finite>F(1,2**45)
# Execute literal small two-slot assembly and validate equal-lengthed gates,
# independent signs and SAM-only support. Use exact rational orthogonal G.
sam=(0,1,2);powers=(5,7);slot=11
def factory():
    yield {'op':'B82_CUT','name':a.CUTS[0]}
    yield a.gate('G',3)
    yield {'op':'B82_CUT','name':a.CUTS[1]}
def leaves(leg,sign):
    return [g for tree in a.with_q_slots(factory,sam,powers,slot,leg=leg,sign=sign) for g in a.old.a41.e.leaves(tree)]
rows={(leg,sign):leaves(leg,sign) for leg,sign in (('Qb','plus'),('Qb','minus'),('Qf','plus'),('Qf','minus'),('centre','centre'))}
assert all(len(row)==2*slot+1 for row in rows.values())
for row in rows.values():
    assert row[slot]=={'op':'G','wires':[3]}
    assert all(set(g['wires']).issubset(set(sam)) for g in row[:slot]+row[slot+1:])
R=sp.Rational;rot=sp.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]])
def matrix(g):
    x=sp.zeros(16)
    for col in range(16):
        if g['op']=='CX':
            c,t=g['wires'];out=col^((1<<t) if col>>c&1 else 0);x[out,col]=1
        else:
            assert g['op']=='G';q=g['wires'][0];b=col>>q&1
            for bit in range(2):x[(col & ~(1<<q)) | (bit<<q),col]=rot[bit,b]
    return x
def product(row):
    out=sp.eye(16)
    for g in row:out=matrix(g)*out
    return out
m={key:product(row) for key,row in rows.items()}
assert m['Qf','minus']==m['Qb','plus']
assert m['Qf','plus']==m['Qb','minus']
assert m['Qb','plus']!=m['Qb','minus']
paths=[Path(__file__),A/'round43/local_q_price.py',A/'round33/SAMPLING_SOURCE_BIAS_RU.md',
 A/'round37/ACTUAL_POST_SAM_STATIONARY_REDUCTION_RU.md',A/'round42/fixed_post_paid_family.py',
 P/'../round84/B84_UNIFORM_ADJACENT_SOURCE_RU.md']
out={'status':'PASS_CONDITIONAL_J2_BUDGET_AND_LITERAL_SMALL_SLOT_ASSEMBLY',
 'pointwise_f_q_derivative_and_adjacent_M_ratio':True,'old_sampling_bias_to_fixed_post_reduced_bound':True,
 'finite_Q_price_lower_greater_than_2^-45':True,'actual_small_slot_recipe_equal_length':True,
 'opposite_logical_Q_sign_same_complete_unitary_exactly':True,
 'consumed_geometric_scalar_source_and_A33_A37_premises':True,
 'production_word_or_full_heat_trace_materialized':False,'full_original_task_marked_map_admission':False,
 'GR_closed':False,'source_sha256':{str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
(P/'B85_A43_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
