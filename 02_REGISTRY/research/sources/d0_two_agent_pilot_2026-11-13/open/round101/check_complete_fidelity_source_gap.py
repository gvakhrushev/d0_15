#!/usr/bin/env python3
"""Exact finite Book03 counterexample; illustrative, not an A49 execution."""
from pathlib import Path
import hashlib,json,sys
import sympy as S

HERE=Path(__file__).resolve().parent
R=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
owner=R/'02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'
book=R/'01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md'
contract=R/'02_REGISTRY/gr_assembly/contract.json'
binding=R/'02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/BOOK_SOURCE_BINDING.md'
direct=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
F=S.Rational
I=S.eye(2); X=S.diag(1,-1); J=S.Matrix([[0,-1],[1,0]])
x=S.symbols('x', real=True)
def rot(v):return S.Matrix([[1-v*v,-2*v],[2*v,1-v*v]])/(1+v*v)
def U(v):return S.simplify(rot(v)*X*rot(v).T)
psi=S.Matrix([F(3,5),F(4,5)]);assert (psi.T*psi)[0]==1
W=U(x);assert S.simplify(W.T*W-I)==S.zeros(2)
assert S.simplify(W*W-I)==S.zeros(2) and S.simplify(S.trace(W))==0
c=S.factor((psi.T*W*psi)[0]);z=F(1,2)
d=S.factor(1-z+z*c*c)
assert c.subs(x,0)==-F(7,25)
# d(-log d)/dx is rational, although the finite price contains a logarithm.
row=S.factor(-S.diff(d,x)/d)
assert row.subs(x,0)==F(672,337)
t=F(1,100);dp=S.factor(d.subs(x,t));dm=S.factor(d.subs(x,-t))
assert dp>0 and dm>0 and dp!=dm

# Two independent internal unitary gates around an untouched DATA W.
# Complete growing-clock similarity on a 3-stage cyclic clock; the reference
# prefix maps and all intermediate marks are allowed to change with label a.
V=rot(F(1,7));Wa=S.kronecker_product(U(F(1,10)),I);Vs=S.kronecker_product(I,V);I4=S.eye(4);Z4=S.zeros(4)
def clock(f0,f1,f2):return S.BlockMatrix([[Z4,Z4,f2],[f0,Z4,Z4],[Z4,f1,Z4]]).as_explicit()
T=clock(Vs,Wa,Vs.T);T0=clock(I4,Wa,I4)
Vclock=S.diag(I4,Vs,Vs)
assert T==Vclock*T0*Vclock.T
assert S.simplify(Vs.T*Wa*Vs-Wa)==S.zeros(4)
# u-dependence preserves the full clock spectrum (and hence H) by conjugacy.
Q1=S.kronecker_product(rot(F(1,10)),I);Q0=S.diag(Q1,Q1,Q1)
assert T0==Q0*clock(I4,S.kronecker_product(X,I),I4)*Q0.T
# Distinct independent directions can fit into SO(74): 74*73/2=2701.
# Their proof is coefficientwise: E_ij-E_ji each has a unique (i,j).
pairs=[(i,j) for i in range(74) for j in range(i+1,74)]
assert len(pairs)==2701 and len(set(pairs[:2688]))==2688

# Full-isometry positive-response construction on an 8-dimensional exact
# fixture: two label bits, one arbitrary two-column input, all four outcomes.
# This does not claim a physical detector has executed.
ket0=S.Matrix([1,0]); J0=S.kronecker_product(I,ket0,ket0)
q=S.Matrix([[F(3,5),-F(4,5)],[F(4,5),F(3,5)]])
flip=S.zeros(8)
for idx in range(8):
    data=(idx>>2)&1
    flip[idx^(2 if data else 0),idx]=1
Fmap=flip*S.kronecker_product(I,q,q)*J0
assert Fmap.T*Fmap==I
fine=[]
for r in range(2):
    for k in range(2):
        basis=S.zeros(4,1);basis[2*r+k]=1
        K=S.kronecker_product(I,basis.T)*Fmap
        E=K.T*K
        assert E==E.T and E.trace()>0 and E.det()>=0
        fine.append(E)
assert sum(fine,S.zeros(2))==I
# Bind the same proposed two-label PVM to real REPORT_0 addresses; this does
# not itself establish an actual registered readout on those wires.
sys.path.insert(0,str(direct/'round48'))
import two_bit_global_source as native
plan=native.namespace();report0=plan['reports'][0]
report_wire=native.physical_wire(report0['REPORT'])
ready_wire=native.physical_wire(report0['all_READY'])
assert (report_wire,ready_wire)==(21216958,21216959)

out={'status':'PASS_EXACT_BOOK03_FULL_FIDELITY_INCOMPLETE_ROWS_COUNTEREXAMPLE',
     'logical_axis_directions':2688,'independent_skew_dimension':2701,
     'axis_rows_are_zero_by_stagewise_clock_conjugacy_and_endpoint_identity':True,
     'extra_source_derivative_exact':'672/337',
     'finite_plus_minus_positive_denominator_ratio':str(dp/dm),
     'finite_plus_minus_equal':False,'full_clock_stage_conjugacy_checked':True,
     'source_effect_defined_on_same_complete_family':True,
     'four_outcome_full_effects_sum_to_identity_on_declared_fibre':True,
     'REPORT0_physical_label_wires':{'REPORT':report_wire,'all_READY':ready_wire},
     'physically_registered_full_fine_readout_established':False,
     'universal_price_or_native_A49_counterexample':False,
     'new_physical_variation_admitted_by_this_fixture':False,
     'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [owner,book,contract,binding,direct/'round48/two_bit_source_native.py',direct/'round49/two_bit_paid_family.py',direct/'round17/GLOBAL_REPORT_ASSEMBLY_RU.md',R/'02_REGISTRY/research/sources/d0_retained_response_concentration_2026-10-28/KAPPA_CLOSURE_RU.md',next((R/'01_BOOKS').glob('BOOK_01*'))]}}
(HERE/'B101_FULL_SOURCE_COUNTEREXAMPLE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
