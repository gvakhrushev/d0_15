#!/usr/bin/env python3
"""Exact finite checks for the clean-sector and rank-two rebit proof."""
from pathlib import Path
from hashlib import sha256
from itertools import product
from fractions import Fraction
import importlib.util,json,sys
import sympy as s
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
O=P.parent
B=O/'round74/lazy_anchor_phase.py'
spec=importlib.util.spec_from_file_location('b74_owned',B);b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

# Exact zero-predicate permutation on all bits. Phase comparator F;phase;F^-1
# restores all computational bits, but the flag's phase-control is correct
# only on the promised clean scratch/flag slice.
def apply(reg,ops):
    for op,*w in ops:
        if op=='X': reg ^= 1<<w[0]
        elif op=='CX':
            if reg>>w[0]&1: reg ^= 1<<w[1]
        else:
            assert op=='CCX'
            if reg>>w[0]&1 and reg>>w[1]&1: reg ^= 1<<w[2]
    return reg
counterexample=None
for n in range(3,7):
    controls=range(n); flag=n; work=range(n+1,2*n-1)
    f=list(b.zero_predicate_ir(controls,flag,work)); finv=list(b.zero_predicate_ir(controls,flag,work,True))
    assert finv==list(reversed(f))
    for bits in range(1<<n):
        for dirty in range(1<<(n-2)):
            reg=bits | (dirty<<(n+1))
            mid=apply(reg,f); active=(mid>>flag)&1
            assert apply(mid,finv)==reg
            if dirty==0: assert active==(bits==0)
            elif active != (bits==0) and counterexample is None:
                counterexample={'N':n,'controls_bits':bits,'scratch_bits':dirty,
                                'flag':0,'actual_phase_bit':active,'desired_phase_bit':int(bits==0)}
assert counterexample is not None

# Exact fixed point identity. q=e^(iπ/3) has q²-q+1=0. For initial
# failure probability e, output bad amplitude multiplier is q*e.
q,e=s.symbols('q e'); f=1+(q-1)*(q*(1-e)+e)
assert s.rem(s.expand(f-q*e),q*q-q+1,q)==0
assert Fraction(5,9)**3<Fraction(1,4)
assert Fraction(5,9)**(3**9)<Fraction(1,2**13122)

# Concrete complex-linear 2D fixture; arbitrary real rebit is the realification
# of the full complex line, and the range projector is rank two. A nonzero
# global phase is immaterial to that rank-two range.
I=s.I; alpha=(1+I*s.sqrt(3))/2
v=s.Matrix([s.Rational(4,5), s.Rational(3,5)])
w=alpha*v
R=lambda z:s.Matrix([[s.re(z),-s.im(z)],[s.im(z),s.re(z)]])
V=s.Matrix.vstack(R(v[0]),R(v[1])); W=s.Matrix.vstack(R(w[0]),R(w[1]))
assert s.simplify(V.T*V)==s.eye(2) and s.simplify(W.T*W)==s.eye(2)
assert s.simplify(V*V.T-W*W.T)==s.zeros(4)
assert (V*V.T).rank()==2
T=s.Matrix.vstack(s.eye(2),s.zeros(2))
projector_delta=V*V.T-T*T.T
assert projector_delta*projector_delta==s.Rational(9,25)*s.eye(4)
# Thus the reflection norm is 2*sqrt(epsilon) = 6/5 here; tensoring an
# arbitrary reference/helper keeps the same bound.
assert (2*projector_delta)*(2*projector_delta)==s.Rational(36,25)*s.eye(4)
# Contrast the incorrect projector that also fixes the rebit to |0>.
col=V[:,0]; assert (col*col.T).rank()==1 and col*col.T != V*V.T

# Weighted selector compressed on clean work/branch is exactly
# (aI+M)/(1+a) on all input data columns.
a,m0,m1=s.symbols('a m0 m1',positive=True)
beta=s.Matrix([s.sqrt(a/(1+a)),1/s.sqrt(1+a)])
embed=s.kronecker_product(beta,s.eye(2)); select=s.diag(1,1,m0,m1)
assert s.simplify(embed.T*select*embed-(a*s.eye(2)+s.diag(m0,m1))/(1+a))==s.zeros(2)

files=[Path(__file__),B,O/'round75/B75_INDEPENDENT_A38_AUDIT_RU.md',O/'round75/B75_INDEPENDENT_ANGLE_AUDIT.json']
out={'status':'PASS_EXACT_FINITE_FIXTURES_AND_SYMBOLIC_IDENTITIES',
     'fixed_point_failure_recursion':'epsilon_next=epsilon^3',
     'shared_clean_scratch_correct_for_all_control_inputs':True,
     'dirty_scratch_counterexample':counterexample,
     'arbitrary_rebit_projector_rank':2,
     'reflection_distance_fixture_is_2_sqrt_epsilon':True,
     'global_rebit_phase_cancels':True,
     'weighted_lcu_block_identity':True,
     'full_a39_emitter_checked':False,'native_schedule_claimed':False,
     'physical_C_closed':False,'GR_closed':False,
     'source_sha256':{str(p):sha256(p.read_bytes()).hexdigest() for p in files}}
(P/'B76_SCOPE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'dirty_scratch_counterexample':counterexample}))
