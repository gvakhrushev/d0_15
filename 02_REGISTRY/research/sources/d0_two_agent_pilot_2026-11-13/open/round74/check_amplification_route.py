#!/usr/bin/env python3
"""Exact finite fixtures and honest resource/precondition accounting."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from math import comb
from hashlib import sha256
import importlib.util,json,sys
import sympy as s
P=Path(__file__).resolve().parent;O=P.parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('anchor',P/'lazy_anchor_phase.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
# Exact primitive logical emitted sequence, clean scratch, all input/flag bits.
for k in range(3,8):
    controls=range(k);flag=k;work=range(k+1,2*k-1)
    ops=list(m.zero_predicate_ir(controls,flag,work))
    inv=list(m.zero_predicate_ir(controls,flag,work,True))
    assert inv==list(reversed(ops))
    counts=Counter(q[0] for q in ops)
    assert counts=={'X':2,'CX':2*k-1,'CCX':2*k-3}
    for bits in range(1<<k):
        for f in (0,1):
            reg=bits|(f<<flag)
            for op,*w in ops:
                if op=='X':reg^=1<<w[0]
                elif op=='CX':
                    if reg>>w[0]&1:reg^=1<<w[1]
                else:
                    if (reg>>w[0]&1) and (reg>>w[1]&1):reg^=1<<w[2]
            assert reg==bits|((f^(bits==0))<<flag)
# All native compact DAG leaves belong to original alphabet for small case;
# the actual k integers here are toy values, NOT new production certificates.
controls=range(3);flag=3;work=range(4,5);rebit=5;aux=6;port=7;spin=(8,9)
actual=list(m.zero_phase_native(controls,flag,work,rebit,1,1,aux,port,spin))
split=len(list(m.zero_predicate_ir(controls,flag,work)))
assert actual[split+1:]==[m.nb.inverse_literal(q,port,spin) for q in reversed(actual[:split])]
for tree in actual:
    for leaf in m.nb.leaves(tree):assert leaf['op'] in ('G','CX','SourceI')
# Actual W good probability >=(2/3)^2; pi/3 fixed point epsilon -> epsilon^3.
# After 9 rounds sqrt(2 eps) <2^-6560 by (5/9)^3 <1/4.
assert F(5,9)**3<F(1,4)
assert (F(5,9)**(3**9))<F(1,2**13122)
# Half vector success=(1+d)/2>3/4 in A37 local chart, 8 rounds.
assert (F(1,4)**(3**8))==F(1,2**13122)
# Explicit B39 recursion word multiplicities including inverse-depth counts.
for L in (8,9):
    counts=[comb(L,d)*2**(L-d) for d in range(L+1)]
    assert sum(counts)==3**L
L,H=9,8
plain=2*3**L;controlled=2*3**(L+H)
assert plain==39366 and controlled==258280326
# Better route: one fixed-point-prepared (c_ref I+M)psi, then ONE
# reflection. Its A9 and literal inverse contain 2*3^9 controlled-W-derived
# occurrences.  This is NOT an expansion into individual G/CX calls.
lcu_controlled=2*3**9
assert lcu_controlled==39366
inv_depth=[comb(9,d)*2**(9-d) for d in range(10)]
full_depth=[(inv_depth[d] if d<=9 else 0)+(inv_depth[d-1] if 0<=d-1<=9 else 0) for d in range(11)]
assert sum(full_depth)==lcu_controlled
# Rank-2 rebit isometry can lose its common phase from the projected range.
X=s.Matrix([1,0]);Y=s.Matrix([s.Rational(3,5),s.Rational(4,5)])
J=s.eye(2);Rx=J-2*X*X.T;Ry=J-2*Y*Y.T
h=(X+Y)/s.sqrt(((X+Y).T*(X+Y))[0]);Rh=J-2*h*h.T
assert Rh*Ry*Y==X and Rx*Ry*Y!=X
# Different phase-rebit states entangle the two half-vector branches: the
# 2x2 matrix of SAM x rebit coefficients has nonzero determinant.
rebit0=s.Matrix([1,0]);rebit90=s.Matrix([0,1])
state=(X*rebit0.T+Y*rebit90.T)/2
assert state.det()!=0
aligned=(X*rebit90.T+Y*rebit90.T)/2
assert aligned.det()==0
# LCU branch: beta=(sqrt(c/(1+c)),sqrt(1/(1+c))), and the compressed
# controlled-W selector produces (c I+M)/(1+c), not M itself.
cc=s.symbols('cc',positive=True);m0,m1=s.symbols('m0 m1',real=True)
beta=s.Matrix([s.sqrt(cc/(1+cc)),s.sqrt(1/(1+cc))])
diagM=s.diag(m0,m1);selector=s.diag(1,1,m0,m1)
embed=s.kronecker_product(beta,s.eye(2))
assert (embed.T*selector*embed-(cc*s.eye(2)+diagM)/(1+cc)).applyfunc(s.simplify)==s.zeros(2)
# Positive M>=2/3 and inherited c_ref>2/3 imply success norm >2/3;
# the normalized bisector perturbation is <=9 sigma²/4, so two-sided
# projector difference is <5 sigma² <2^-6025 with inherited sigma bound.
assert F(4,3)/2==F(2,3)
sigma=F(1,2**3014);assert 5*sigma*sigma<F(1,2**6025)
aa,rr=s.symbols('aa rr',positive=True);p0,p1,e0,e1=s.symbols('p0 p1 e0 e1',real=True)
ps=s.Matrix([p0,p1]);ev=s.Matrix([e0,e1]);va=(aa+rr)*ps+ev;vr=2*rr*ps+ev
tau=(aa+rr)/(2*rr)
assert (va-tau*vr-(rr-aa)*ev/(2*rr)).applyfunc(s.simplify)==s.zeros(2,1)
# U_alt is a different full operator in general even when its action on
# the occupied vector is the desired one: P may rotate a perpendicular plane.
chi=s.Matrix([0,0,1]);rot=s.Matrix([[0,-1,0],[1,0,0],[0,0,1]])
ident=s.eye(3);Rchi=ident-2*chi*chi.T
u_alt=Rchi*rot.T*Rchi
assert u_alt*chi==chi and u_alt!=ident
# A sufficient final target-operator tolerance for two endpoint J values:
# (1/(2 d0 c_ref))*eps/(g s t) <2^-74, using d0>3/4,c_ref>2/3.
err=F(1,2**4850);scale=err*2**3158*2**1618
assert scale==F(1,2**74)
# If the full new post circuit is real/unitary and acts on SAM+fresh-private
# only, the full-vector preparation error e gives exact c/r=1-e²/2, even
# when private leaks.  The normalization absorbs the retained probability.
ee,rr=s.symbols('ee rr',nonnegative=True,real=True)
loss=s.expand(rr**2-(rr*(1-ee**2/2))**2)
assert s.expand(loss-rr**2*(ee**2-ee**4/4))==0
e_fd=F(1,2**2425)
assert e_fd*e_fd*2**3158*2**1618/2==F(1,2**75)
# Post skew derivative is O(e), so its requirement remains stricter.
e_post=F(1,2**3232)
assert e_post*2**3158==F(1,2**74)
# Actual controls: W is A30 WORK = n_total - 2688; large AND is linear,
# not a numerical phase certificate for K~10^10.
n=10407050782;mwork=n-2688
assert mwork==10407048094 and mwork.bit_length()==34
for k in (n,mwork):
    assert 2*k-3>0 and 2*k-1>0 and k-2>0
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
files=[P/'check_amplification_route.py',P/'lazy_anchor_phase.py',D/'round13/reversible_selectors.py',D/'round14/native_boolean.py',D/'round21/CHOI_ASSEMBLY_CONTRACT_RU.md',D/'round22/FULL_RAW_CHOI_RU.md',D/'round29/G_CX_ONLY_REALIZATION_RU.md',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',D/'round37/ACTUAL_POST_SAM_STATIONARY_REDUCTION_RU.md',O/'round39/OMEGA_HALF_ADAPTER_RU.md',O/'round39/adapter_native.py',O/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',O/'round72/B72_BACKWARD_MARKED_OUTPUT_SUBSYSTEM_RU.md',root/'02_REGISTRY/research/sources/d0_native_readiness_amplification_2026-10-24/PHASE_COMPILER.md']
out={'status':'PARTIAL_NATIVE_ANCHOR_EMITTER_AND_FIXED_POINT_ROUTE_NOT_FULL_USTAR','A30_total_births':n,'A30_WORK_bits':mwork,'zero_predicate_clean_work':'N-2','zero_predicate_counts':'2 X, 2N-1 CX, 2N-3 CCX, followed by literal inverse','weighted_LCU_target':'(c_ref I+M)psi/(1+c_ref)','weighted_LCU_success_amplitude_gt':'2/3','weighted_LCU_fixed_point_levels':9,'ideal_weighted_LCU_prep_error_lt':'2^-6560 before native errors','LCU_controlled_W_derived_blocks_for_single_reflection':lcu_controlled,'half_replacement_reflection_error_lt':'2^-6025 conditional on A37 sigma','alternative_stationary_target_same_full_operator_as_A37_Ustar_proved':False,'two_stage_xi_levels':L,'two_stage_half_levels':H,'two_stage_uncontrolled_W_derived_blocks':plain,'two_stage_controlled_W_derived_blocks':controlled,'existing_B39_accepts_actual_WORK_width':False,'new_precision_phase_or_controlled_W_certificates_generated':False,'two_stage_relative_rebit_phase_alignment_required':True,'LCU_rank_two_rebit_global_phase_cancels_conditionally':True,'sufficient_per_endpoint_operator_error_for_generic_fd_normalized_error_lt_2^-74':'2^-4850, conditional on original gs/t/c_ref and same eta retention','full_real_vector_error_e_gives_exact_c_over_r':'1-e²/2 without dropping private failure','sufficient_full_vector_error_e_each_endpoint_for_feedback_fd_error_lt_2^-75':'2^-2425 under stated matching and normalization','sufficient_full_vector_error_for_unit_skew_post_feedback_row_lt_2^-74':'2^-3232, with fixed actual U and specified canonical input','quadratic_finite_loss_does_not_prove_post_stationarity':True,'actual_full_Ustar_native_word_emitted':False,'native_same_task_admission_and_full_price_proved':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in files}}
(P/'AMPLIFICATION_ROUTE_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'LCU_controlled_W_derived_blocks':lcu_controlled,'prepared_native_Ustar':False}))
